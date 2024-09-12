from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('success/', views.booking_success, name='booking-success'),
    path('failed/', views.booking_failed, name='booking-failed'),
    path('bookings/', views.booking_list, name='booking_list'),
]