# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm

"""@login_required
def seller_dashboard(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden()
    products = request.user.products.all()
    return render(request, 'sellerapp/seller_dashboard.html', {'products': products})
"""
@login_required
def seller_dashboard(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("You are not authorized to view this page")
    
    products = request.user.products.all()
    return render(request, 'seller_app/seller_dashboard.html', {'products': products})


@login_required
def add_product(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)#request.FILES used for image handling. Ajesh
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'seller_app/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'seller_app/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'seller_app/delete_product.html', {'product': product})
