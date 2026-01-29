from django.urls import path
from cart.views import *

urlpatterns = [
    path("", cart , name='cart'),
    path("add_to_cart", add_to_cart, name='add_to_cart'),
    path("checkout/", checkout, name='checkout'),
    path('process_checkout/', process_checkout, name='process_checkout'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path('order_placed/<int:order_id>/', order_placed, name='order_placed')
]