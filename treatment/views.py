from django.shortcuts import render
from .models import Product
from django.db.models import Q

def all_products(request):
    query = request.GET.get('q')  
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(additional_info__icontains=query)  
        )
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'treatment/all_products.html', context)

