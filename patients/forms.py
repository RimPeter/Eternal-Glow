from django import forms
from .models import PatientInformation

class PatientInformationForm(forms.ModelForm):
    class Meta:
        model = PatientInformation
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'email',
            'address',
            'medical_history',
            'allergies',
            'current_medications',
            'primary_physician',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'medical_history': forms.Textarea(attrs={'rows': 4}),
            'allergies': forms.Textarea(attrs={'rows': 4}),
            'current_medications': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
