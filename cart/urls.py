from django.urls import path
from cart.views import cart, add_to_cart, process_checkout, checkout

urlpatterns = [
    path("", cart , name='cart'),
    path("add_to_cart", add_to_cart, name='add_to_cart'),
    path("checkout/", checkout, name='checkout'),
    path('process_checkout/', process_checkout, name='process_checkout'),
]

