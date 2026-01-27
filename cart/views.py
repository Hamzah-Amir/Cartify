from django.shortcuts import render
from .models import CartItem

# Create your views here.

def cart(request):
    if request.method == "GET":
        cart = CartItem.objects.all()
        return render(request, 'cart/cart.html', {"cart": cart})