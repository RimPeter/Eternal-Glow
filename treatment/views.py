from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from .models import Product, Category, BodyPart

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

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'treatment/product_detail.html', {'product': product})

def all_products(request):
    products = Product.objects.all()
    return render(request, 'treatment/all_products.html', {'products': products})

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'treatment/all_categories.html', {'categories': categories})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    return render(request, 'treatment/category_detail.html', {'category': category})

def all_bodyparts(request):
    bodyparts = BodyPart.objects.all()
    return render(request, 'treatment/all_bodyparts.html', {'bodyparts': bodyparts})

def bodypart_detail(request, id):
    bodypart = get_object_or_404(BodyPart, id=id)
    return render(request, 'treatment/bodypart_detail.html', {'bodypart': bodypart})

def anti_aging(request):
    return render(request, 'treatment/anti_aging.html')

def body(request):
    return render(request, 'treatment/body.html')

def injectables(request):
    return render(request, 'treatment/injectables.html')

def laser(request):
    return render(request, 'treatment/laser.html')

def skin(request):
    return render(request, 'treatment/skin.html')


