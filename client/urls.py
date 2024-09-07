from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-admin/', views.register_admin, name='register_admin'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('login/', auth_views.LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='client/logout.html'), name='logout'),
    ]
