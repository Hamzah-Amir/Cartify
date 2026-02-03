from django.shortcuts import render, redirect
from products.models import Product


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

    # Static dummy data for layout; replace with real queryset later
    context = {
        "products": [
            {
                "name": "Premium Wireless Headphones",
                "category": "Electronics",
                "price": "$299.99",
                "stock": 45,
                "status": "active",
                "created": "2024-01-15",
            },
            {
                "name": "Leather Laptop Bag",
                "category": "Accessories",
                "price": "$149.99",
                "stock": 23,
                "status": "active",
                "created": "2024-01-14",
            },
            {
                "name": "Smart Watch Pro",
                "category": "Electronics",
                "price": "$399.99",
                "stock": 0,
                "status": "inactive",
                "created": "2024-01-12",
            },
            {
                "name": "Minimalist Desk Lamp",
                "category": "Home & Office",
                "price": "$79.99",
                "stock": 67,
                "status": "active",
                "created": "2024-01-10",
            },
            {
                "name": "Organic Cotton T-Shirt",
                "category": "Clothing",
                "price": "$29.99",
                "stock": 120,
                "status": "active",
                "created": "2024-01-08",
            },
        ]
    }
    return render(request, "seller/products.html", context)

def orders(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')

    context = {
        "orders": [
            {
                "order_id": "ORD-001",
                "buyer_name": "John Smith",
                "buyer_email": "john.smith@email.com",
                "items": 2,
                "total": "$459.97",
                "date": "2024-01-20",
                "status": "completed",
            },
            {
                "order_id": "ORD-002",
                "buyer_name": "Sarah Johnson",
                "buyer_email": "sarah.j@email.com",
                "items": 1,
                "total": "$149.99",
                "date": "2024-01-22",
                "status": "shipped",
            },
            {
                "order_id": "ORD-003",
                "buyer_name": "Michael Brown",
                "buyer_email": "mbrown@email.com",
                "items": 1,
                "total": "$89.97",
                "date": "2024-01-23",
                "status": "processing",
            },
            {
                "order_id": "ORD-004",
                "buyer_name": "Emily Davis",
                "buyer_email": "emily.davis@email.com",
                "items": 1,
                "total": "$299.99",
                "date": "2024-01-24",
                "status": "pending",
            },
        ]
    }
    return render(request, "seller/orders.html", context)