import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cartify.settings')
django.setup()

from products.models import Product, ProductImage

# Get all products with their additional images
products = Product.objects.all()
for p in products:
    print(f"Product: {p.name}")
    print(f"  Primary image: {p.image.url}")
    print(f"  Additional images: {p.additional_images.count()}")
    for img in p.additional_images.all():
        print(f"    - {img.image.url}")
    print()
