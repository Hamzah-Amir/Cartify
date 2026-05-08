from django.contrib import admin
from users.models import CustomUser
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from products.models import *

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4
    fields = ('image',)
    max_num = 4
    verbose_name_plural = "Additional Product Images (Max 4)"


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'seller', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'created_at', 'seller')
    search_fields = ('name', 'description', 'seller__username')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'seller', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Primary Image', {
            'fields': ('image',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProductImageInline]

class ProductResource(resources.ModelResource):

    seller = fields.Field(attribute='seller', column_name='Seller Username', widget=ForeignKeyWidget(CustomUser, 'username'))
    def before_import_row(self, row, **kwargs):
        seller_username = row.get('Seller Username')
        if seller_username:
            try:
                seller = CustomUser.objects.get(username=seller_username)
                if seller.role != "seller":
                    raise ValueError(f"User '{seller_username} on row {row}' is not a seller.")
            except CustomUser.DoesNotExist:
                raise ValueError(f"User '{seller_username} on row {row}' does not exist.")

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)