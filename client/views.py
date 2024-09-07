from django.contrib.auth import login
from .forms import AdminRegistrationForm
from .forms import PatientForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PatientForm
from .models import Patient



def home(request):
    return render(request, 'client/home.html')

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('home')  # Replace with the URL to redirect after successful registration
    else:
        form = AdminRegistrationForm()
    return render(request, 'client/register_admin.html', {'form': form})

@login_required
def register_patient(request):
    if Patient.objects.filter(user=request.user).exists():
        # If the patient already exists, redirect to a different page or show a message
        return redirect('my_details')
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Associate with the logged-in user
            patient.save()
            form.save_m2m()  # Save many-to-many relationships (medical conditions)
            return redirect('my_details')  # Redirect after successful registration
    else:
        form = PatientForm()
    return render(request, 'client/register_patient.html', {'form': form})

def login(request):
    return render(request, 'client/login.html')

def logout(request):
    return render(request, 'client/logout.html')

@login_required
def my_details(request):
    patient_qs = Patient.objects.filter(user=request.user)

    if not patient_qs.exists():
        # If no patient is found, handle accordingly (redirect or show message)
        return redirect('register_patient')

    # If there are multiple patient records, just get the first one
    patient = patient_qs.prefetch_related('medical_conditions').first()
    context = {
        'patient': patient,
        'medical_conditions': patient.medical_conditions.all(), 
    }
    return render(request, 'client/my_details.html', context)

@login_required
def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('my_details')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'client/register_patient.html', {'form': form})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    if request.method == 'POST':
        patient.delete()
        return redirect('home')

    return render(request, 'client/confirm_delete.html', {'patient': patient})
