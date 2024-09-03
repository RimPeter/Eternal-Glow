from django.shortcuts import render, redirect
from .forms import PatientInformationForm

def home(request):
    return render(request, 'patients/home.html')

def register_patient(request):
    if request.method == 'POST':
        form = PatientInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients:home')
    else:
        form = PatientInformationForm()
    return render(request, 'patients/register_patient.html', {'form': form})