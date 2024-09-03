from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_patient/', views.register_patient, name='register_patient'),
]
