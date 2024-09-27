from django.urls import path
from . import views

urlpatterns = [
    path('all-products/', views.all_products, name='all_products'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('categories/', views.all_categories, name='all_categories'),
    path('categories/<int:id>/', views.category_detail, name='category_detail'),
    path('bodyparts/', views.all_bodyparts, name='all_bodyparts'),
    path('bodyparts/<int:id>/', views.bodypart_detail, name='bodypart_detail'),
    path('anti-aging/', views.anti_aging, name='anti_aging'),
    path('body/', views.body, name='body'),
    path('injectables/', views.injectables, name='injectables'),
    path('laser/', views.laser, name='laser'),
    path('skin/', views.skin, name='skin'),
]

    