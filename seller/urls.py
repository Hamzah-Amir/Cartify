from django.urls import path
from seller.views import dashboard, inventory, orders, manage_order

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("inventory/", inventory, name="inventory"),
    path("orders/", orders, name="orders"),
    path("orders/<int:order_id>/detail/", manage_order, name="manage_order"),
]
