from django.contrib import admin
from django.db.models import CharField
from django.forms import Select
from users.models import CustomUser
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from products.models import *

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)
    max_num = 4
    verbose_name_plural = "Additional Images"


class ProductAdmin(ImportExportModelAdmin):
    resource_class = None
    
    # List view configuration
    list_display = ('name', 'seller', 'price', 'stock', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'seller')
    search_fields = ('name', 'description', 'seller__username')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    # Detail view configuration - Clean and organized
    fieldsets = (
        ('Product Details', {
            'fields': ('id', 'name', 'seller', 'category', 'status'),
            'description': 'Basic information about the product'
        }),
        ('Description & Images', {
            'fields': ('description', 'image'),
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('id', 'created_at')
    inlines = [ProductImageInline]
    
    # Fix dropdown display issue
    formfield_overrides = {
        CharField: {'widget': Select},
    }
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ensure category and status dropdowns display selected values
        if 'category' in form.base_fields:
            form.base_fields['category'].widget.attrs.update({'class': 'form-control'})
        if 'status' in form.base_fields:
            form.base_fields['status'].widget.attrs.update({'class': 'form-control'})
        return form


class ProductResource(resources.ModelResource):
    seller = fields.Field(attribute='seller', column_name='seller', widget=ForeignKeyWidget(CustomUser, 'username'))

    def before_import_row(self, row, **kwargs):
        seller_username = row.get('seller')
        if seller_username:
            try:
                seller = CustomUser.objects.get(username=seller_username)
                if seller.role != "seller":
                    raise ValueError(f"User '{seller_username}' is not a seller.")
            except CustomUser.DoesNotExist:
                raise ValueError(f"User '{seller_username}' does not exist.")

    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'category', 'image', 'stock', 'seller')
        export_order = ('name', 'price', 'description', 'category', 'image', 'stock', 'seller')
        import_id_fields = ()
        skip_unchanged = True
        report_skipped = False

# Customize admin site
admin.site.site_header = "Cartify Admin"
admin.site.site_title = "Cartify"
admin.site.index_title = "Welcome to Cartify Admin"

ProductAdmin.resource_class = ProductResource

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)