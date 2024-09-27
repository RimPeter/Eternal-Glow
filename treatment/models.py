from django.urls import reverse
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])


class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse('bodypart_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    body_part = models.ForeignKey(BodyPart, on_delete=models.SET_NULL, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in minutes")
    additional_info = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.product_name
