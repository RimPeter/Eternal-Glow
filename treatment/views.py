from django.shortcuts import render
from .models import Product
from django.db.models import Q

def all_products(request):
    query = request.GET.get('q') 
    sort_by = request.GET.get('sort')
    products = Product.objects.all()
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(additional_info__icontains=query)  
        )
    else:
        products = Product.objects.all()
        
    if sort_by == 'price_asc':
        products = products.order_by('price')  
    elif sort_by == 'price_desc':
        products = products.order_by('-price')  
    elif sort_by == 'duration_asc':
        products = products.order_by('duration') 
    elif sort_by == 'duration_desc':
        products = products.order_by('-duration')
    context = {'products': products}
    return render(request, 'treatment/all_products.html', context)

