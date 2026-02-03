from django.shortcuts import render, redirect


def dashboard(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    if request.user.role != 'seller':
        return redirect('home')
    return render(request, 'seller/dashboard.html')


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