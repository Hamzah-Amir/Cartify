from .models import WishlistItem
from cart.models import CartItem

def wishlist_count(request):
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {"wishlist_count": count}

def cart_count(request):

    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else: 
        count = 0
        
    return {"cart_count": count}