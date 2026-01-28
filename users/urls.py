from django.urls import path
from users.views import *

urlpatterns = [
    path('register/role', role, name='role'),
    path('register/form', registerUser, name='registerUser'),
    path('login/', loginUser, name='loginUser'),
    path('logout/', logoutUser, name='logout'),
    path('profile/', profile, name="profile"),
    path('wishlist', wishlist, name='wishlist'),
    path('add_to_wishlist', add_to_wishlist, name='add_to_wishlist'),
]