from django.contrib import admin
from .models import Booking, TimeSlot

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'product', 'booking_date', 'time_slot', 'payment_status', 'booked_on')
    search_fields = ('patient__first_name', 'patient__last_name', 'product__product_name')
    list_filter = ('payment_status', 'booking_date')
    date_hierarchy = 'booking_date'

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('slot',)

admin.site.site_header = "Clinic Booking System"
admin.site.site_title = "Clinic Booking System"
admin.site.index_title = "Welcome to Clinic Booking System"

