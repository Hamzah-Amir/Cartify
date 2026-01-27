from django.urls import path
from seller.views import *

urlpatterns = [
    path('', seller, name='seller')
]
