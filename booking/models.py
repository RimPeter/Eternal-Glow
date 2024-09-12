from django.db import models
from client.models import Patient  # Importing the Patient model from the client app
from treatment.models import Product  # Importing the Product model from the treatment app
from django.core.exceptions import ValidationError
from datetime import date

class TimeSlot(models.Model):
    slot = models.CharField(max_length=99, help_text="Enter time slot (e.g., 09:00 AM - 10:00 AM)")

    def __str__(self):
        return self.slot


class Booking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    booking_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    booked_on = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('patient', 'booking_date')  # Ensure no duplicates at the DB level
        
    def clean(self):
        today = date.today()
        if self.booking_date is None:
            raise ValidationError("Booking date is in the past.")

        if self.booking_date <= today:
            raise ValidationError("Booking date cannot be today or in the past.")

        if self.time_slot is None:
            raise ValidationError("A time slot must be selected.")
        
    def __str__(self):
        return f"Booking for {self.patient} on {self.booking_date} at {self.time_slot}"
