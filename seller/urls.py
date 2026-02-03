from django.urls import path
from seller.views import dashboard, products

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("products/", products, name="seller_products"),
]
