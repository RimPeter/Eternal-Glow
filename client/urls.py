from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-admin/', views.register_admin, name='register_admin'),
    path('register/', views.register_admin, name='register'),
    ]
