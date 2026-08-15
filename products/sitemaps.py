from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from products.models import CATEGORY, Product


class ProductSitemap(Sitemap):
    """Every in-stock, active product detail page."""
    changefreq = "daily"
    priority = 0.8
    protocol = "https"
    limit = 5000

    def items(self):
        return Product.objects.filter(status="active", stock__gt=0).order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("productDetail", args=[obj.id])


class CategorySitemap(Sitemap):
    """The filtered listing pages, e.g. /?category=electronics"""
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def items(self):
        return [slug for slug, label in CATEGORY]

    def location(self, item):
        return "{}?category={}".format(reverse("home"), item)


class StaticViewSitemap(Sitemap):
    """Public pages worth indexing.

    Login / register / cart / seller pages are deliberately left out: they are
    thin or private, and they carry a noindex tag anyway.
    """
    changefreq = "daily"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)
