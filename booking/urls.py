from django.urls import path
from . import views

urlpatterns = [
    #create booking:
    path('create/', views.create_booking, name='create_booking'),
    path('failed/', views.booking_failed, name='booking-failed'),
    path('bookings/', views.booking_list, name='booking_list'),
    
    #stripe:
    path('create-checkout-session/<int:booking_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:booking_id>', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    
    #manage booking:
    path('manage-booking/<int:booking_id>/', views.manage_booking, name='manage_booking'),
    path('change-booking-date/<int:booking_id>/', views.change_booking_date, name='change_booking_date'),
    path('change-booking-product/<int:booking_id>/', views.change_booking_product, name='change_booking_product'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('product-change-success/<int:booking_id>/<int:new_product_id>/', views.product_change_success, name='product_change_success'),
]
