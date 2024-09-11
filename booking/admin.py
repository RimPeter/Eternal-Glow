from django.contrib import admin
from .models import Timetable, Booking


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('date', 'time')  
    list_filter = ('date',)  
    search_fields = ('date',)  

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'price', 'get_booking_time') 
    list_filter = ('product', 'user')  
    search_fields = ('user__username', 'product__product_name')  
    filter_horizontal = ('timetables',)  

    def get_booking_time(self, obj):
        return obj.get_booking_time()  
    get_booking_time.short_description = 'Booking Time'

admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Booking, BookingAdmin)
