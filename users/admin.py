from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import CharField
from django.forms import Select
from .models import CustomUser, WishlistItem

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined', 'gender')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    list_per_page = 25
    
    fieldsets = (
        ('Account Info', {
            'fields': ('username', 'email', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'gender', 'age', 'profile_image'),
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'address', 'city', 'state', 'postal_code'),
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Delivery Settings', {
            'fields': ('base_delivery_fee',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create User', {
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    # Fix dropdown display for role
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'role' in form.base_fields:
            form.base_fields['role'].widget.attrs.update({'class': 'form-control'})
        if 'gender' in form.base_fields:
            form.base_fields['gender'].widget.attrs.update({'class': 'form-control'})
        return form


class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'get_product_price')
    list_filter = ('user', 'product__category')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('user', 'product')
    
    def get_product_price(self, obj):
        return f"₨ {obj.product.price}"
    get_product_price.short_description = 'Product Price'


# Customize admin site
admin.site.site_header = "Cartify Admin"
admin.site.site_title = "Cartify"
admin.site.index_title = "Welcome to Cartify Admin"

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)