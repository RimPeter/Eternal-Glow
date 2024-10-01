from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Product, TimeSlot, Booking
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
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
import logging

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

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
    if hasattr(request.user, 'patient'):
        bookings = Booking.objects.filter(patient=request.user.patient).order_by('-booked_on') 
        context = {
            'bookings': bookings
        }
        return render(request, 'booking/booking_list.html', context)
    else:
        messages.warning(request, "Please complete your patient profile before accessing your bookings.")
        return redirect('register_patient')
    
@login_required
def create_checkout_session(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    price_in_pennies = int(booking.product.price * 100)
    
    try:
        # Build the path to the success view
        path = reverse('payment_success', args=[booking.id])
        # Construct the success URL without encoding the placeholder
        success_url = f"{request.build_absolute_uri(path)}?session_id={{CHECKOUT_SESSION_ID}}"
        
        # Optionally, print the success_url for debugging
        print('Success URL:', success_url)
        
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
        
        # Do not set booking.stripe_payment_intent_id here
        return redirect(session.url)
    
    except Exception as e:
        return render(request, 'booking/payment_error.html', {'error': str(e)})

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.error(request, "No session ID provided.")
        return redirect('booking_list')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent_id = session.payment_intent
    except stripe.error.StripeError as e:
        messages.error(request, "Error retrieving session information.")
        return redirect('booking_list')

    if not payment_intent_id:
        messages.error(request, "No payment intent found in session.")
        return redirect('booking_list')

    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except stripe.error.StripeError as e:
        messages.error(request, "Error retrieving payment information.")
        return redirect('booking_list')

    if payment_intent.status == 'succeeded':
        booking.payment_status = True
        booking.stripe_payment_intent_id = payment_intent_id
        booking.save()
        return render(request, 'booking/payment_success.html', {'booking': booking})
    else:
        messages.error(request, "Payment was not successful.")
        return redirect('booking_list')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.debug(f"Received Stripe event: {event['type']}")
    except ValueError:
        logger.error("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature")
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_intent_failed(payment_intent)
    else:
        logger.warning(f"Unhandled event type: {event['type']}")

    return HttpResponse(status=200)

logger = logging.getLogger(__name__)
def handle_payment_intent_succeeded(payment_intent):
    booking_id = payment_intent.metadata.get('booking_id')
    logger.debug(f"Handling payment_intent.succeeded for booking_id: {booking_id}")

    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = True
            booking.stripe_payment_intent_id = payment_intent.id
            booking.save()
            logger.info(f"Payment succeeded for Booking ID {booking_id}.")
        except Booking.DoesNotExist:
            logger.error(f"Booking with ID {booking_id} does not exist.")
    else:
        logger.error("No booking_id found in PaymentIntent metadata.")

def handle_payment_intent_failed(payment_intent):
    booking_id = payment_intent.metadata.get('booking_id')

    if booking_id:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = False
            booking.save()
            logger.info(f"Payment failed for Booking ID {booking_id}.")
        except Booking.DoesNotExist:
            logger.error(f"Booking with ID {booking_id} does not exist.")

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

                # Step 1: Build the base URL
                path = reverse('product_change_success', args=[booking.id, new_product.id])
                base_url = request.build_absolute_uri(path)

                # Step 2: Append the session_id parameter without encoding braces
                success_url = f"{base_url}?session_id={{CHECKOUT_SESSION_ID}}"

                # Optionally, print the success_url for debugging
                print('Success URL:', success_url)

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

from django.contrib import messages
import stripe

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, patient=request.user.patient)
    today = datetime.date.today()

    if booking.booking_date <= today:
        messages.error(request, "You cannot cancel the booking on the same day.")
        return redirect('manage_booking', booking_id=booking.id)

    if request.method == 'POST':
        if booking.payment_status:
            # Process a refund
            try:
                refund = stripe.Refund.create(
                    payment_intent=booking.stripe_payment_intent_id,
                    amount=int(booking.product.price * 100),  # Amount in cents
                )
                # Optionally, store refund details in your database
                # booking.refund_id = refund.id
                # booking.save()
                
                # Add a message with the 'refund' tag
                messages.success(
                    request,
                    "Booking canceled successfully. A refund will be processed within the next six days.",
                    extra_tags='refund'
                )
            except Exception as e:
                messages.error(request, "There was an error processing your refund. Please contact support.")
                return redirect('manage_booking', booking_id=booking.id)
        else:
            # Booking was unpaid
            messages.success(request, "Booking canceled successfully.")

        # Delete the booking after processing
        booking.delete()
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

    try:
        # Retrieve the Checkout Session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as e:
        messages.error(request, "Error retrieving session information.")
        return redirect('manage_booking', booking_id=booking.id)

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