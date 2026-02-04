from django.shortcuts import render, redirect
from products.models import Product, ProductImage
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

def add_listing(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')
    if request.method == "GET" and request.user.is_authenticated and request.user.role == 'seller':
        return render(request, "seller/add_listing.html")
    if request.method == "POST" and request.user.is_authenticated and request.user.role == 'seller':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        additional_images = request.FILES.getlist('additional_images')
        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            image=image,
            seller=request.user,
        )
        for additional_image in additional_images:
            ProductImage.objects.create(
                product=product,
                image=additional_image,
            )
        return redirect('dashboard')