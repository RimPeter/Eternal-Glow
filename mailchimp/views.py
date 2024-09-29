from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MailchimpSubscribeForm
from .mailchimp_utils import subscribe_email

def subscribe_view(request):
    if request.method == "POST":
        form = MailchimpSubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            response = subscribe_email(email)
            
            # Check if the subscription was successful
            if response.status_code == 200:
                messages.success(request, "You have been successfully subscribed!")
            elif response.status_code == 400:
                error_message = response.json().get('detail', 'An error occurred')
                messages.error(request, f"Error: {error_message}")
            else:
                messages.error(request, "An unexpected error occurred. Please try again later.")
            
            return redirect('subscribe')
    
    else:
        form = MailchimpSubscribeForm()
    
    return render(request, 'mailchimp/subscribe.html', {'form': form})
