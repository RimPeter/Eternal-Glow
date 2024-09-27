from django.contrib import admin
from client import views as client_views
from django.urls import path, include, re_path
from django.urls.conf import include 
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from treatment.sitemaps import (
    ProductSitemap,
    CategorySitemap,
    BodyPartSitemap,
    StaticViewSitemap,
)
import os

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'bodyparts': BodyPartSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('client.urls')),
    path('treatment/', include('treatment.urls')),
    path('accounts/', include('allauth.urls')),
    path('booking/', include('booking.urls')),
    path('robots.txt', client_views.robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.views.static import serve
    import os
    from django.urls import re_path
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))

    urlpatterns += [
        re_path(r'^robots\.txt$', serve, {
            'path': 'robots.txt',
            'document_root': os.path.join(settings.BASE_DIR, 'static'),
        }),
        re_path(r'^favicon\.ico$', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(settings.BASE_DIR, 'static'),
        }),
    ]