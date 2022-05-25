import json
import random
import string
import stripe
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import View, ListView, DetailView
from .models import *
from .forms import *


# Create your views here.
def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))



def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class ShopView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'shop.html'




def item_detail(request, pk):
    object = Item.objects.get(pk=pk)
    return render(request, 'product-details.html', {'item':object})
@never_cache
def cart(request):
    orderItems = OrderItem.objects.all()
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    return render(request, 'cart.html', {'orderItems':orderItems, 'order':order})

def add_single_to_cart(request, pk):
    item = Item.objects.get(pk=pk)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)
    orderItem.quantity += 1
    orderItem.save()
    return redirect('cart')

def remove_single_from_cart(request, pk):
    item = Item.objects.get(pk=pk)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)
    orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return redirect('cart')

def add_more_to_cart(request, pk):
    print(request.POST['quantity'])
    item = Item.objects.get(pk=pk)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)
    orderItem.quantity += int(request.POST['quantity'])
    orderItem.save()
    return redirect('cart')
@login_required
def checkout(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    return render(request, 'checkout.html', {'order':order})









