from django.shortcuts import render, redirect
from users.models import CustomUser, WishlistItem
from products.models import Product
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def role(request):
    return render(request, 'users/role.html')

def registerUser(request):

    # Writing backend of authentication
    role = request.GET.get('role') if request.method == 'GET' else request.POST.get('role')
    if not role:
        return redirect('role')
    
    if request.method == 'GET':
        return render(request, 'users/register.html', {'role': role})
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                "username_error": "Username Already Exist",
                "role": role,
                'form_data': request.POST 
                })

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {
                "email_error": "Email Already Exist",
                "role": role,
                'form_data': request.POST 
                })

        if CustomUser.objects.filter(phone_number=phone).exists():
            return render(request, 'users/register.html', {
                "number_error": "Number Already registered",
                "role": role,
                'form_data': request.POST 
                })


        user = CustomUser.objects.create_user(username=username,
                                               email=email,
                                               first_name=first_name,
                                               last_name=last_name,
                                               password=password,
                                               role=role,
                                               gender=gender,
                                               age=age,
                                               phone_number=phone)
        user.save()
        return redirect('loginUser')

    return redirect('role')

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('loginUser')
    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect("loginUser")


def profile(request):
    if request.method == "GET":
        return render(request, 'users/profile.html')
    
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.gender = request.POST.get('gender')
        user.age = request.POST.get('age')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return render(request, "users/profile.html")
    
def wishlist(request):
    if request.method == "GET" and request.user.is_authenticated:
        wishlistitem = WishlistItem.objects.filter(user=request.user)
        print("wishlistitem", wishlistitem)
        return render(request, "users/wishlist.html", {"wishlist": wishlistitem})

    if request.method == "POST" and request.user.is_authenticated:
        product = Product.objects.get(id=request.POST.get('product_id'))
        already_exist = WishlistItem.objects.filter(product=product, user=request.user).exists()
        if already_exist:
            WishlistItem.objects.filter(user=request.user, product=product).delete()
        else:
            wishlists = WishlistItem.objects.create(user=request.user, product=product)
        return redirect("wishlist")
    else:
        redirect("loginUser")
