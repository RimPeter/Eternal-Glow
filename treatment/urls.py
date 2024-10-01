from django.urls import path
from . import views

urlpatterns = [
    path('all-products/', views.all_products, name='all_products'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('anti-aging/', views.anti_aging, name='anti_aging'),
    path('injectables/', views.injectables, name='injectables'),
    path('laser/', views.laser, name='laser'),
    path('skin/', views.skin, name='skin'),
    path('categories/<int:id>/', views.category_detail, name='category_detail'),
    path('body-parts/<int:id>/', views.bodypart_detail, name='bodypart_detail'),
    path('body/', views.body, name='body'),
]

    