from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Product, TimeSlot, Booking

import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Booking
import stripe_keys

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
                return redirect('booking-success', booking_id=booking.id)

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
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'booking/booking_success.html', {
        'booking': booking,
        'stripe_public_key': stripe_keys.STRIPE_PUBLISHABLE_KEY  
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
    booking = Booking.objects.get(id=booking_id)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': booking.product.product_name,
                        },
                        'unit_amount': int(booking.product.price * 100),  
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/payment-success/'),  
            cancel_url=request.build_absolute_uri('/payment-cancel/'),    
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
    
def payment_success(request):
    return render(request, 'booking/payment_success.html')

def payment_cancel(request):
    return render(request, 'booking/payment_cancel.html')
