from django.shortcuts import render
from products.models import Product
from django.db.models import Q
from django.core.paginator import Paginator
from users.models import WishlistItem

# Create your views here.

def home(request):
    # Logic for Fetching Products
    if request.method == "GET":
        category = request.GET.get('category')
        search_query = request.GET.get('search')
        
        # Start with base query - only products with stock > 0
        products = Product.objects.filter(stock__gt=0)
        
        # Apply search filter if search query exists
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        
        # Apply category filter if category is specified and valid
        if category == 'grocery-essentials' or category == 'toys-games' or category == 'automotive' or category == 'electronics' or category == 'fashion-apparel' or category == 'home-kitchen' or category == 'beauty-personal-care' or category == 'sports-outdoor' or category == 'books-media' or category == 'misc/other':
            products = products.filter(category=category)
        
        # Pagination
        paginator = Paginator(products, 24)  # Show 24 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            "products": page_obj,
            "page_obj": page_obj,
            "total_products": paginator.count,
            "category": category,
            "search_query": search_query,
        }
        
        return render(request, 'products/home.html', context)

def productDetail(request, uuid):
    id = uuid
    product = Product.objects.prefetch_related('additional_images').filter(id=id).first()
    print(product)

    # Get related products from same category, excluding current product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]

    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()

    return render(request, 'products/productdetail.html', {
        "product": product, 
        "related_products": related_products,
        "in_wishlist": in_wishlist
    })