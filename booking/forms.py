from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from datetime import date, timedelta

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
        max_future_date = today + timedelta(days=60)
        
        
        if not booking_date:
            raise forms.ValidationError("Booking date is required.")

        if booking_date > max_future_date:
            raise forms.ValidationError("You cannot book more than 60 days in advance.")

        if booking_date <= today:
            raise forms.ValidationError("You cannot book for today or any past dates.")

        return booking_date
