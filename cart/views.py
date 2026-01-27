from django.shortcuts import render

# Create your views here.

def cart(request):
    if request.method == "GET":
        return render(request, 'cart/cart.html')