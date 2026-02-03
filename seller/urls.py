from django.urls import path
from seller.views import dashboard, inventory, orders, order_detail

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("inventory/", inventory, name="inventory"),
    path("orders/", orders, name="orders"),
    path("orders/<int:order_id>/detail/", order_detail, name="order_detail"),
]
