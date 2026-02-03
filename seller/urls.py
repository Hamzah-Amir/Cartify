from django.urls import path
from seller.views import dashboard, inventory

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("inventory/", inventory, name="inventory"),
]
