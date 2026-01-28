from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from products.models import Product

# Create your views here.

def cart(request):
    if request.method == "GET":
        cart = CartItem.objects.all()
        price = 0
        for item in cart:
            price += item.product.price * item.quantity
        return render(request, 'cart/cart.html', {"cart": cart, "total_price": price})
    

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect("loginUser")
    
    product = get_object_or_404(Product, id=request.POST.get('product_id'))

    item, created = CartItem.objects.get_or_create(
        user=request.user, 
        product=product
            )
    
    if not created:
        item.quantity += 1
        item.save
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def process_checkout(request):
    if request.method == "GET":
        return render(request, 'cart/checkout.html')