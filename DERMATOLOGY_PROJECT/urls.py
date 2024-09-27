from django.contrib import admin
from client import views as client_views
from django.urls import path, include, re_path
from django.urls.conf import include 
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('client.urls')),
    path('treatment/', include('treatment.urls')),
    path('accounts/', include('allauth.urls')),
    path('booking/', include('booking.urls')),
    path('robots.txt', client_views.robots_txt),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))

    # Serve robots.txt and favicon.ico at the root URL
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