from django.contrib import admin

from .models import Product, City, Category

admin.site.register(Product)
admin.site.register(City)
admin.site.register(Category)
