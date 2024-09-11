from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from datetime import datetime, date
from django.db.models import Q
from treatment.models import Product

class Timetable(models.Model):
    date = models.DateField()  
    time = models.TimeField()  

    class Meta:
        unique_together = ('date', 'time')  

    def __str__(self):
        return f"{self.date} - {self.time.strftime('%H:%M')}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    timetables = models.ManyToManyField(Timetable)  
    
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically allocate time slots based on product duration.
        """
        if not self.pk:  # Ensure this is a new booking
            if self.timetables.exists():
                start_slot = self.timetables.first()
                required_slots = self.get_required_slots()
                end_slot = self.allocate_time_slots(start_slot, required_slots)
                if not end_slot:
                    raise ValueError("Not enough consecutive time slots available.")
        super().save(*args, **kwargs)

    def get_required_slots(self):
        """
        Calculate how many 30-minute slots are required based on the product duration.
        """
        return (self.product.duration // 30) + (1 if self.product.duration % 30 else 0)

    def allocate_time_slots(self, start_slot, required_slots):
        """
        Allocate consecutive time slots starting from the given slot.
        """
        available_slots = Timetable.objects.filter(
            date=start_slot.date, 
            time__gte=start_slot.time
        ).order_by('time')[:required_slots]

        if len(available_slots) == required_slots:
            # Assign these time slots to the booking
            self.timetables.set(available_slots)
            return available_slots[-1]  # Return the last time slot (end time slot)
        return None

    def get_booking_time(self):
        """
        Returns a string representing the time range of the booking based on timetables.
        """
        times = self.timetables.order_by('time')
        if times.exists():
            start_time = times.first().time
            end_time = (datetime.combine(date.today(), times.last().time) + 
                        timedelta(minutes=30)).time()
            return f"{start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}"
        return "No time selected"

    def __str__(self):
        return f"Booking by {self.user.username} for {self.product.product_name} on {self.get_booking_time()}"
