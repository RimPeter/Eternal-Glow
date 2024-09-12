from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['product', 'time_slot', 'booking_date', 'additional_notes']
        widgets = {
            'booking_date': forms.SelectDateWidget(),
            'additional_notes': forms.Textarea(attrs={'rows': 4}),
        }
