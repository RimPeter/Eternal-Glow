from django.db import models

class PatientInformation(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    
    # Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    # Medical Information
    medical_history = models.TextField(blank=True, help_text="Summary of the patient's medical history.")
    allergies = models.TextField(blank=True, help_text="List any known allergies.")
    current_medications = models.TextField(blank=True, help_text="List any current medications.")
    primary_physician = models.CharField(max_length=100, blank=True)
    
    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['last_name', 'first_name']


