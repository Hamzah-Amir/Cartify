from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Order, OrderItem
from collections import defaultdict
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
    
from collections import defaultdict
from django.db.models import Sum

def process_checkout(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return redirect('cart')

    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('cart')

    # Group cart items by seller
    seller_groups = defaultdict(list)
    for ci in cart_items:
        seller_groups[ci.product.seller].append(ci)

    orders_created = []

    for seller, items in seller_groups.items():
        # calculate total for this seller
        total = sum(ci.product.price * ci.quantity for ci in items)

        # create Order per seller
        order = Order.objects.create(
            user=user,
            total_price=total,
            status="unpaid"
        )

        # create OrderItems
        for ci in items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price
            )

        orders_created.append(order)

    # clear cart
    cart_items.delete()

    return render(request, 'cart/process_checkout.html', {
        "orders": orders_created,   # list of orders (one per seller)
        "delivery_fee": 150
    })

def order_detail(request, order_id):
    if request.method == "GET" and request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)

        return render(request, 'cart/order_detail.html', {
            "order": order,
            "order_items": order_items,
        })

def order_placed(request, order_id):
    if request.method == "GET":
        order = get_object_or_404(Order, id=order_id, user=request.user)

        return render(request, 'cart/order_placed.html', {"order": order})