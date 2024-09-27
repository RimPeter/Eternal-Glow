from django.contrib.auth import login
from .forms import AdminRegistrationForm
from .forms import PatientForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, ChangePasswordForm
from .models import Patient
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse




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
        messages.info(request, "You already have a patient profile.")
        return redirect('my_details')
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Associate with the logged-in user
            patient.save()
            form.save_m2m()  # Save many-to-many relationships (medical conditions)
            messages.success(request, "Your patient profile has been created.")
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

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password1')
            
            user = request.user
            
            if not user.check_password(old_password):
                form.add_error('old_password', 'Old password is incorrect')
            else:
                user.set_password(new_password)
                user.save()
                
                update_session_auth_hash(request, user)
                
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('password_change_success')  
    else:
        form = ChangePasswordForm()

    return render(request, 'client/change_password.html', {'form': form})

def password_change_success(request):
    return render(request, 'client/password_change_success.html')

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'The user has been deleted successfully.')
        return redirect('home') 
    
    return render(request, 'client/confirm_delete_user.html', {'user': user})

def robots_txt(request):
    content = "User-agent: *\nDisallow: /admin/\n"
    return HttpResponse(content, content_type="text/plain")