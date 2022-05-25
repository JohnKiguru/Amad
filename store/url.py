from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('<pk>/detail', views.item_detail, name='product-detail'),
    path('<pk>/add_single_to_cart', views.add_single_to_cart, name='add_single_to_cart'),
    path('<pk>/remove_single_from_cart', views.remove_single_from_cart, name='remove_single_from_cart'),
    path('<pk>/add_more_to_cart', views.add_more_to_cart, name='add_more_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout')

]
