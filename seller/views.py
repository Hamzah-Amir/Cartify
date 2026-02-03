from django.shortcuts import render, redirect
from products.models import Product
from cart.models import Order


def dashboard(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')
    if request.method == "GET" and request.user.is_authenticated and request.user.role == 'seller':
        products = Product.objects.filter(seller=request.user)
        active_listing = Product.objects.filter(status="active")
        context = {
            "products" : products,
            "total_products" : len(products),
            "active_listing": len(active_listing),
        }
        print(context)
        return render(request, 'seller/dashboard.html', context)


def inventory(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')
    if request.method == "GET" and request.user.is_authenticated and request.user.role == 'seller':
        products = Product.objects.filter(seller=request.user)
        context = {
            "products": products
        }
        return render(request, "seller/inventory.html", context)

def orders(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')

    if request.method == "GET" and request.user.is_authenticated and request.user.role == 'seller':
        orders = Order.objects.filter(user=request.user)
        context = {
            "orders": orders
        }
        print(context)
        return render(request, "seller/orders.html", context)

def manage_order(request, order_id):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')

    if request.method == "GET" and request.user.is_authenticated and request.user.role == 'seller':
        order = Order.objects.get(id=order_id)
        context = {
            "order": order
        }
        print(context)
        return render(request, "seller/order_detail.html", context)
