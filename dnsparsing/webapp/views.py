from django.shortcuts import render

from .models import Product

def index(request):
    products_list = Product.objects.order_by('product_price')
    return render(request,'webapp/index.html',{'products_list':products_list})
