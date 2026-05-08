from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import CharField
from django.forms import Select, ModelForm
from .models import CustomUser, WishlistItem


class CustomUserForm(ModelForm):
    """Custom form to ensure Gender and Role fields display properly"""
    class Meta:
        model = CustomUser
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure gender field shows current value
        if self.instance and self.instance.pk:
            if 'gender' in self.fields:
                self.fields['gender'].initial = self.instance.gender
            if 'role' in self.fields:
                self.fields['role'].initial = self.instance.role


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserForm
    list_display = ('username', 'email', 'role', 'gender', 'is_active', 'date_joined')
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
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'gender'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')


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