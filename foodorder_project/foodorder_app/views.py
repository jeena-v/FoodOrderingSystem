from django.shortcuts import render
from seller_app.models import Product

def index(request):
    
    return render(request, 'foodorder_app/index.html')

def menu(request):
    products = Product.objects.all()
    return render(request, 'foodorder_app/menu.html',{'products':products})

def about(request):
    return render(request, 'foodorder_app/about.html')




