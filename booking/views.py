from django.shortcuts import render

def booking(request):
    return render(request, 'booking/create_booking.html')