from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, MedicalCondition

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = False  # Set as staff automatically
        user.is_superuser = False  # Ensure they are not superuser
        if commit:
            user.save()
        return user



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name',
            'date_of_birth',  # Single date field for Date of Birth
            'gender', 'phone',
            'house_number', 'street_name', 'post_code',
            'medical_conditions'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # Date selector widget
            'medical_conditions': forms.CheckboxSelectMultiple,  # Multiple checkboxes for medical conditions
        }
