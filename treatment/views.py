from django.shortcuts import render
from .models import Product
# Create your views here.

def all_products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'treatment/all_products.html', context)

