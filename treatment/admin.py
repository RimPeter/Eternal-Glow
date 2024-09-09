from django.contrib import admin
from .models import Product, Category, BodyPart


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(BodyPart)