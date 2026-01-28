from django.urls import path
from cart.views import cart, add_to_cart

urlpatterns = [
    path("", cart , name='cart'),
    path("add_to_cart", add_to_cart, name='add_to_cart')
]

