from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
