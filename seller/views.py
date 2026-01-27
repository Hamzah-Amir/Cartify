from django.shortcuts import render, redirect

# Create your views here.

def seller(request):
    if request.user.is_anonymous:
        return redirect('loginUser')
    return render(request, 'seller/seller_dashboard.html')