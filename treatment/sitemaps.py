# treatment/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category, BodyPart

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at 

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

class BodyPartSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BodyPart.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['all_products', 'anti_aging', 'body', 'injectables', 'laser', 'skin']

    def location(self, item):
        return reverse(item)
