from django.db import models
from uuid import uuid4

# Create your models here.

CATEGORY = [("electronics", "Electronics"), ("fashion-apparel", "Fashion & Apparel"), ("home-kitchen", "Home & Kitchen"), ("toys-games", "Toys & Games"), ("beauty-personal-care", "Beauty & Personal Care"), ("sports-outdoors", "Sports & Outdoors"), ("books-media", "Books & Media"), ("grocery-essentials", "Grocery & Essentials"), ("automotive", "Automotive"), ("misc/other", "Misc / Other")]

class Product(models.Model):
    STATUS = [("active", "Active"), ("closed", "Closed")]
    seller = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='products')
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    category = models.CharField(max_length=100, null=False, choices=CATEGORY)
    status = models.CharField(max_length=15, null=False, choices=STATUS, default="active")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
    
    def __str__(self):
        return f"Image for {self.product.name}"