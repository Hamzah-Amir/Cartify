from django.db import models
from users.models import CustomUser
from django.db.models import Max
from products.models import Product
import uuid

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    PAYMENT_METHODS = [
        ('online', 'Online Payment'),
        ('cod', 'Cash on Delivery'),
    ]
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending_review")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='online')
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.aggregate(max_id=Max('id'))['max_id'] or 0
            self.order_number = f"ORD-{last_order + 1:05d}"  # ORD-00001, ORD-00002
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # freeze price at checkout