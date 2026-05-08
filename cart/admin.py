from django.contrib import admin
from .models import *

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('added_at', 'product__category')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('user', 'product', 'added_at')
    date_hierarchy = 'added_at'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number', 'user', 'created_at', 'total_price')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status', 'created_at'),
        }),
        ('Pricing', {
            'fields': ('total_price', 'delivery_fee', 'payment_method'),
        }),
    )
    
    inlines = [OrderItemInline]
    
    def total_price(self, obj):
        return f"₨ {obj.total_price if hasattr(obj, 'total_price') else 'N/A'}"
    total_price.short_description = 'Total Price'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__created_at', 'product__category')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('order', 'product', 'quantity', 'price')


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)