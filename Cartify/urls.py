"""
URL configuration for Cartify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve

from products.sitemaps import CategorySitemap, ProductSitemap, StaticViewSitemap

# Used by /sitemap.xml so search engines can discover every public page
sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('', include('products.urls')),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('seller/', include('seller.urls')),
    path('cart/', include('cart.urls')),
]

# Serving uploaded media files.
#
# django.conf.urls.static.static() returns an EMPTY list when DEBUG is False,
# so it only ever worked in development - which is why product images 404'd in
# production. WhiteNoise does not serve MEDIA_ROOT either (it is for static
# files only), so we add an explicit route.
#
# Django's serve() view is not built for high traffic. It is fine for a small
# portfolio site; put the media directory behind nginx or a CDN before this
# gets real traffic.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]