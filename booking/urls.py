from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    #path('booking-success/<int:booking_id>/', views.booking_success, name='booking-success'),
    path('failed/', views.booking_failed, name='booking-failed'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('create-checkout-session/<int:booking_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:booking_id>', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]