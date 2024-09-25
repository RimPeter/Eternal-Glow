from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Product, TimeSlot, Booking
from django.urls import reverse

import stripe
from .models import Booking
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from client.models import Patient  
from client.forms import PatientForm
from django.contrib import messages
import datetime 
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


@login_required
def create_booking(request):
    product_id = request.GET.get('product')  
    selected_product = None
    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        
    time_slots = TimeSlot.objects.all()
        
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            if hasattr(request.user, 'patient'):
                booking.patient = request.user.patient

                # Check for duplicate booking
                if Booking.objects.filter(patient=booking.patient, booking_date=booking.booking_date).exists():
                    messages.error(request, "You already have a booking on this date.")
                    return redirect('booking-failed')
                else:
                    booking.payment_status = False  
                    booking.save()
                    return redirect('create_checkout_session', booking_id=booking.id)
            else:
                messages.warning(request, "Please complete your patient profile before booking.")
                return redirect('register_patient')

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

#stripe.api_key = stripe_keys.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    price_in_pennies = int(booking.product.price * 100)
    
    try:
        success_url = request.build_absolute_uri(reverse('payment_success', args=[booking.id]))
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
            success_url=success_url,
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            metadata={"booking_id": booking.id, "user_id": request.user.id}
        )
        
        booking.stripe_payment_intent_id = session.payment_intent
        booking.save()
        
        return redirect(session.url)
    
    except Exception as e:
        return render(request, 'booking/payment_error.html', {'error': str(e)})

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment_intent = stripe.PaymentIntent.retrieve(booking.stripe_payment_intent_id)

    if payment_intent.status == 'succeeded':
        booking.payment_status = True
        booking.save()
        return render(request, 'booking/payment_success.html', {'booking': booking})
    else:
        messages.error(request, "Payment was not successful.")
        return redirect('booking_list')

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

        if not booking.payment_status:
            # Booking is unpaid
            booking.product = new_product
            booking.save()
            messages.success(request, "Product changed successfully. Please proceed to payment when ready.")
            return redirect('manage_booking', booking_id=booking.id)

        else:
            # Booking is paid
            if price_difference == 0:
                # No price difference, simply update the product
                booking.product = new_product
                booking.save()
                messages.success(request, "Product changed successfully.")
                return redirect('manage_booking', booking_id=booking.id)

            elif price_difference > 0:
                # Additional payment required
                success_url = request.build_absolute_uri(
                    reverse('product_change_success', args=[booking.id, new_product.id]) + '?session_id={CHECKOUT_SESSION_ID}'
                )
                try:
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=[
                            {
                                'price_data': {
                                    'currency': 'gbp',
                                    'product_data': {
                                        'name': f"Additional Payment for {new_product.product_name}",
                                    },
                                    'unit_amount': int(price_difference * 100),
                                },
                                'quantity': 1,
                            },
                        ],
                        mode='payment',
                        success_url=success_url,
                        cancel_url=request.build_absolute_uri(reverse('manage_booking', args=[booking.id])),
                        metadata={"booking_id": booking.id, "user_id": request.user.id, "new_product_id": new_product.id}
                    )
                    # Store the session ID in the session for later verification
                    request.session['additional_payment_session_id'] = session.id
                    return redirect(session.url)
                except Exception as e:
                    messages.error(request, "There was an error processing your payment. Please try again.")
                    return redirect('manage_booking', booking_id=booking.id)

            elif price_difference < 0:
                # Process a partial refund
                refund_amount = abs(price_difference)
                try:
                    refund = stripe.Refund.create(
                        payment_intent=booking.stripe_payment_intent_id,
                        amount=int(refund_amount * 100),
                    )
                    # Update the booking with the new product
                    booking.product = new_product
                    booking.save()
                    messages.success(request, f"Product changed successfully. A refund of £{refund_amount} will be processed within the next 5 working days.")
                    return redirect('manage_booking', booking_id=booking.id)
                except Exception as e:
                    messages.error(request, "There was an error processing your refund. Please contact support.")
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
            pass

        booking.delete()

        messages.success(request, "Booking canceled successfully.")
        return redirect('booking_list')

    else:
        return redirect('manage_booking', booking_id=booking.id)

@login_required
def product_change_success(request, booking_id, new_product_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    new_product = get_object_or_404(Product, id=new_product_id)

    # Retrieve the Checkout Session ID from the URL parameters
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Unable to verify payment.")
        return redirect('manage_booking', booking_id=booking.id)

    # Retrieve the Checkout Session from Stripe
    session = stripe.checkout.Session.retrieve(session_id)

    # Verify that the payment was successful
    if session.payment_status == 'paid':
        # Update the booking with the new product
        booking.product = new_product
        booking.save()

        messages.success(request, "Product changed successfully after additional payment.")
        return redirect('manage_booking', booking_id=booking.id)
    else:
        messages.error(request, "Payment was not successful.")
        return redirect('manage_booking', booking_id=booking.id)
    
def payment_cancel(request):
    return render(request, 'booking/payment_cancel.html')

@login_required
def create_patient_profile(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, "Your patient profile has been created.")
            return redirect('create_booking')  # Redirect back to booking page
    else:
        form = PatientForm()
    return render(request, 'patient/create_patient_profile.html', {'form': form})