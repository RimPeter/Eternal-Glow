from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Product, TimeSlot, Booking
from django.urls import reverse

import stripe
from .models import Booking
import stripe_keys
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
import datetime 


@login_required
def create_booking(request):
    product_id = request.GET.get('product')  # Get the product ID from the query parameters
    selected_product = None
    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        
    time_slots = TimeSlot.objects.all()
        
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
                return redirect('create_checkout_session', booking_id=booking.id)

    else:
        form = BookingForm(initial={'time_slot': time_slots.first()})

    products = Product.objects.all()

    return render(request, 'booking/create_booking.html', {
        'form': form,
        'products': products,
        'time_slots': time_slots,
        'selected_product': selected_product
    })

    
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

stripe.api_key = stripe_keys.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    price_in_pennies = int(booking.product.price * 100)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': booking.product.product_name,
                    },
                    'unit_amount': price_in_pennies,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success', args=[booking.id])),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        metadata={"booking_id": booking.id, "user_id": request.user.id}
    )
    
    return redirect(session.url)

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Update booking payment status
    booking.payment_status = True
    booking.save()
    return render(request, 'booking/payment_success.html', {'booking': booking})

def payment_cancel(request):
    return render(request, 'booking/payment_cancel.html')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    return None

def handle_checkout_session(session):
    return None

@login_required
def manage_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    products = Product.objects.all()
    time_slots = TimeSlot.objects.all()
    today = datetime.date.today()

    return render(request, 'booking/manage_booking.html', {
        'booking': booking,
        'products': products,
        'time_slots': time_slots,
        'today': today
    })
    
@login_required
def change_booking_date(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    today = datetime.date.today()

    if booking.booking_date <= today:
        messages.error(request, "You cannot change the booking on the same day.")
        return redirect('manage_booking', booking_id=booking.id)

    if request.method == 'POST':
        new_date_str = request.POST.get('new_booking_date')
        new_time_slot_id = request.POST.get('new_time_slot')
        if not new_date_str or not new_time_slot_id:
            messages.error(request, "Please select a new date and time slot.")
            return redirect('manage_booking', booking_id=booking.id)
        
        try:
            new_date = datetime.datetime.strptime(new_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('manage_booking', booking_id=booking.id)
        
        new_time_slot = get_object_or_404(TimeSlot, id=new_time_slot_id)

        if new_date <= today:
            messages.error(request, "You cannot select today's date or a past date.")
            return redirect('manage_booking', booking_id=booking.id)

        # Check for conflicting bookings
        conflict = Booking.objects.filter(
            booking_date=new_date,
            time_slot=new_time_slot,
        ).exclude(id=booking.id).exists()
        
        if conflict:
            messages.error(request, "The selected date and time slot is already booked.")
            return redirect('manage_booking', booking_id=booking.id)

        # Update the booking
        booking.booking_date = new_date
        booking.time_slot = new_time_slot
        booking.save()

        messages.success(request, "Booking date and time updated successfully.")
        return redirect('manage_booking', booking_id=booking.id)

    else:
        return redirect('manage_booking', booking_id=booking.id)

@login_required
def change_booking_product(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    today = datetime.date.today()

    if booking.booking_date <= today:
        messages.error(request, "You cannot change the booking on the same day.")
        return redirect('manage_booking', booking_id=booking.id)

    if request.method == 'POST':
        new_product_id = request.POST.get('new_product')
        new_product = get_object_or_404(Product, id=new_product_id)
        # Calculate price difference
        price_difference = new_product.price - booking.product.price

        # Handle additional payment or refund
        if price_difference > 0:
            # Need to collect additional payment
            # Create a new Stripe checkout session for the difference
            # Redirect to the payment page
            pass
        elif price_difference < 0:
            # Need to process a partial refund
            # Use Stripe API to refund the difference
            pass

        # Update the booking with the new product
        booking.product = new_product
        booking.save()

        messages.success(request, "Product changed successfully.")
        return redirect('manage_booking', booking_id=booking.id)

    else:
        return redirect('manage_booking', booking_id=booking.id)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    today = datetime.date.today()

    if booking.booking_date <= today:
        messages.error(request, "You cannot cancel the booking on the same day.")
        return redirect('manage_booking', booking_id=booking.id)

    if request.method == 'POST':
        if booking.payment_status:
            # Process refund via Stripe
            # You need to store the Stripe payment intent ID when the payment is made
            pass

        # Cancel the booking
        booking.delete()

        messages.success(request, "Booking canceled successfully.")
        return redirect('booking_list')

    else:
        return redirect('manage_booking', booking_id=booking.id)
