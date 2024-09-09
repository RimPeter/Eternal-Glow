from django.contrib import admin
from .models import Product, Category, BodyPart


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'body_part', 'price', 'duration')
    list_filter = ('category', 'body_part')
    search_fields = ('product_name', 'category__name', 'body_part__name')
     
    ordering = ('category', 'body_part', 'product_name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(BodyPart)