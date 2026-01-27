from django.urls import path
from cart.views import cart

urlpatterns = [
    path("", cart , name='cart')
]

