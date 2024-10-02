from django.contrib import admin
from .models import MedicalCondition, Patient

admin.site.register(MedicalCondition)
admin.site.register(Patient)
