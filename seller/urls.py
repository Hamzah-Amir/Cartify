from django.urls import path
from seller.views import dashboard, inventory, orders, manage_order, add_listing

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("inventory/", inventory, name="inventory"),
    path("orders/", orders, name="orders"),
    path("orders/<int:order_id>/detail/", manage_order, name="manage_order"),
    path("products/add_listing/", add_listing, name="add_listing"),
]
