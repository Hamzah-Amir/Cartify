from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Order, OrderItem
from .services.pricing import calculate_delivery_fee
from collections import defaultdict
from users.models import CustomUser
from products.models import Product

# Create your views here.

def cart(request):
    if request.method == "GET":
        cart_items = CartItem.objects.filter(user=request.user)  # get only the current user's cart
        total_price = 0
        delivery_fees = defaultdict(int)

        # Group items by seller
        seller_groups = defaultdict(list)
        for item in cart_items:
            seller_groups[item.product.seller].append(item)
            total_price += item.product.price * item.quantity

        # Calculate delivery fee per seller
        for seller, items in seller_groups.items():
            delivery_fees[seller] = calculate_delivery_fee(seller, items)

        total_delivery_fee = sum(delivery_fees.values())

        return render(request, 'cart/cart.html', {
            "cart": cart_items,
            "total_price": total_price,
            "delivery_fee": total_delivery_fee
        })

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
            delivery_fee = calculate_delivery_fee(item.product.seller, cart_items)

        print(user.email, user.user_id)
        return render(request, 'cart/checkout.html', {"user": user, "total_price": price, "delivery_fee": delivery_fee})
    
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

        delivery_fee = calculate_delivery_fee(seller, cart_items)
        
        # Create Order with status "pending_review" to indicate it's awaiting confirmation
        order = Order.objects.create(
            user=user,
            total_price=total,
            delivery_fee=delivery_fee,
            payment_method=request.POST.get('payment_method'),
            status="pending_review"
        )
        
        # Store cart items in order temporarily (we'll create OrderItems in order_detail)
        # Add a reference to the cart items for later processing
        order._pending_cart_items = items
        orders_created.append(order)

    return render(request, 'cart/process_checkout.html', {
        "orders": orders_created,   # list of orders (one per seller)
    })

def order_detail(request, order_id):
    if request.method == "GET" and request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Create OrderItems when order_detail is first accessed (if not already created)
        if order.items.count() == 0 and order.status == "pending_review":
            # Get the cart items for this user that haven't been cleared yet
            cart_items = CartItem.objects.filter(user=request.user)
            
            if cart_items.exists():
                # Create OrderItems from cart items
                for ci in cart_items:
                    # Only add items that belong to this order's seller
                    if ci.product.seller == cart_items.first().product.seller:
                        OrderItem.objects.create(
                            order=order,
                            product=ci.product,
                            quantity=ci.quantity,
                            price=ci.product.price
                        )
                
                # Clear cart after creating order items
                cart_items.delete()
        
        order_items = OrderItem.objects.filter(order=order)

        return render(request, 'cart/order_detail.html', {
            "order": order,
            "order_items": order_items,
        })

def order_placed(request, order_id):
    if request.method == "GET":
        order = get_object_or_404(Order, id=order_id, user=request.user)

        return render(request, 'cart/order_placed.html', {"order": order})