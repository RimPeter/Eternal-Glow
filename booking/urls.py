from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking, name='create_booking'),
]