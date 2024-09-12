from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Product, TimeSlot, Booking

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = request.user.patient

            # Check for duplicate booking
            if Booking.objects.filter(patient=booking.patient, booking_date=booking.booking_date).exists():
                return redirect('booking-failed')
            else:
                booking.payment_status = False  # Set payment status
                booking.save()
                return redirect('booking-success')

    else:
        form = BookingForm()

    products = Product.objects.all()
    time_slots = TimeSlot.objects.all()

    return render(request, 'booking/create_booking.html', {
        'form': form,
        'products': products,
        'time_slots': time_slots,
    })

    
@login_required
def booking_success(request):
    return render(request, 'booking/booking_success.html') 

@login_required
def booking_failed(request):
    return render(request, 'booking/booking_failed.html', {'message': "You already have a booking on this date."})

@login_required
def booking_list(request):
    bookings = Booking.objects.all().order_by('-booked_on') 
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/booking_list.html', context) 