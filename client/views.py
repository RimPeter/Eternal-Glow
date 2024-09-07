from django.contrib.auth import login
from .forms import AdminRegistrationForm
from .forms import PatientForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PatientForm


def home(request):
    return render(request, 'client/home.html')

@login_required
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Associate with the logged-in user
            patient.save()
            form.save_m2m()  # Save many-to-many relationships (medical conditions)
            return redirect('home')  # Redirect after successful registration
    else:
        form = PatientForm()

    return render(request, 'client/register_patient.html', {'form': form})
