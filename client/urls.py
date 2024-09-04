from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_client/', views.register_client, name='register_client'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, next_page='/'), name='login'),
    ]
