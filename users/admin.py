from django.contrib import admin
from .models import CustomUser, WishlistItem

# Register your models here.

admin.site.site_header = "Cartify Admin Panel"
admin.site.site_title = "Cartify Admin Portal"
admin.site.index_title = "Welcome to Cartify Admin Panel"
admin.site.register(CustomUser)
admin.site.register(WishlistItem)