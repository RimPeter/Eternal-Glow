from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-admin/', views.register_admin, name='register_admin'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('client/login/', auth_views.LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='client/logout.html'), name='logout'),
    path('my-details/', views.my_details, name='my_details'),
    path('update-patient/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-change-success/', views.password_change_success, name='password_change_success'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='client/login.html')),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    ]
