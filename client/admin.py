from django.contrib import admin
from .models import MedicalCondition, Patient

# Register the MedicalCondition model in the admin
admin.site.register(MedicalCondition)
admin.site.register(Patient)
