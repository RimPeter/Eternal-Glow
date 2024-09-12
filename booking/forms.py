from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['product', 'time_slot', 'booking_date', 'additional_notes']
        widgets = {
            'booking_date': forms.SelectDateWidget(),
            'additional_notes': forms.Textarea(attrs={'rows': 4}),
        }
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        today = date.today()
        
        # Check if the booking date is today or in the past
        if booking_date <= today:
            raise ValidationError("You cannot book for today or any past dates.")
        
        return booking_date
