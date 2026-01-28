from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Order, OrderItem
from users.models import CustomUser
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
    print(request.POST)

    item, created = CartItem.objects.get_or_create(
        user=request.user, 
        product=product,
        quantity=request.POST.get('quantity')
        )
    
    if not created:
        item.quantity += 1
        item.save
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def checkout(request):
    if request.method == "GET":
        user = CustomUser.objects.get(user_id=request.user.user_id)
        price = 0
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            price += item.product.price * item.quantity

        print(user.email, user.user_id)
        return render(request, 'cart/checkout.html', {"user": user, "total_price": price})
    
def process_checkout(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cart')
        
        order =  Order.objects.create(
            user=user,
            total_price = sum(ci.product.price * ci.quantity for ci in cart_items),
            status='unpaid'
        )

        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price
            )
        cart_items.delete()
        return render(request, 'cart/process_checkout.html')