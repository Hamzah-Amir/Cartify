from django.urls import path
from seller.views import dashboard, inventory, orders

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("inventory/", inventory, name="inventory"),
    path("orders/", orders, name="orders"),
]
