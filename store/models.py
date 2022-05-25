from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('Chairs', 'Chairs'),
    ('Beds', 'Beds'),
    ('Accessories', 'Accessories'),
    ('Furniture', 'Furniture'),
    ('Home Deco', 'Home Deco'),
    ('Dressings', 'Dressings'),
    ('Table', 'Table')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    device = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.device


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer,
                             on_delete=models.CASCADE, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)

    start_date = models.DateTimeField(auto_now_add=True)

    complete = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        return sum([item.get_final_price for item in self.orderitem_set.all()])

    @property
    def get_cart_items(self):
        return sum([item.quantity for item in self.orderitem_set.all()])


class OrderItem(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.item.price

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_item_price - self.get_total_discount_item_price

    @property
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price
        return self.get_total_item_price


class Address(models.Model):
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.codegr


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def customer_receiver(sender, instance, created, *args, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)


post_save.connect(customer_receiver, sender=settings.AUTH_USER_MODEL)
