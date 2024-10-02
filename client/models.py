from django.db import models
from django.contrib.auth.models import User

class MedicalCondition(models.Model):
    condition_name = models.CharField(max_length=100)

    def __str__(self):
        return self.condition_name


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        null=True,  
        blank=False  
    )    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(default="default@example.com")
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=10)
    medical_conditions = models.ManyToManyField(MedicalCondition, blank=True)

    # Date of registration (auto-generated)
    date_of_registration = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_registration})"







