from django.db import models

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # ForeignKey to Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # ForeignKey to BodyPart model, optional field
    body_part = models.ForeignKey(BodyPart, on_delete=models.SET_NULL, blank=True, null=True)

    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Duration in minutes, optional field
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in minutes")
    
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name
