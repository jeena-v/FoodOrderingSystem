# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Product , Category,Cart
from .forms import ProductForm , CategoryForm
from django.contrib.auth import logout


@login_required
def seller_dashboard(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("You are not authorized to view this page")
    
    products = Product.objects.all()
    return render(request, 'seller_app/seller_dashboard.html', {'products': products})
@login_required
def seller_menu(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("You are not authorized to view this page")
    
    products = Product.objects.filter(seller=request.user)  # Only show seller's own products
    categories = Category.objects.all()

    return render(request, 'seller_app/seller_menu.html', {'products': products,'categories':categories})
def menu_detail(request,product_id):
    # Get the product by ID or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Render the product details page with the product information
    return render(request, 'seller_app/menu_detail.html', {'product': product})


@login_required
def add_product(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)#request.FILES used for image handling. 
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

 
# View to list all categories


@login_required
def category_create(request):  #Create the category

    if request.user.user_type != 'seller':
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.seller = request.user
            category.save()
            return redirect('seller_dashboard')
    else:
        form = CategoryForm()
    return render(request, 'seller_app/add_category.html', {'form': form})

    


@login_required
def category_update(request, id):  #Update the category

    category = get_object_or_404(Product, id=id, seller=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'seller_app/edit_category.html', {'form': form})

    
 
@login_required
def category_delete(request, id):  # Delete the category
    category = get_object_or_404(Product, id=id, seller=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('seller_dashboard')
    return render(request, 'seller_app/delete_category.html', {'category': category})


def seller_logout(request):
    # Log out the user
    logout(request)
    # Redirect to the home page or login page after logging out
    return redirect('index')  

def cart(request):
    return render(request,'buyer_app/cart.html')
   


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  

    # Ensure only buyers can add to cart
    if request.user.user_type == 'buyer':  
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    
        return redirect('cart')

    # If user is not a buyer, redirect them (or show an error message)
    return redirect('home')  # Change 'home' to the appropriate page
@login_required
def view_cart(request):
    # Fetch all cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate subtotal
    subtotal = sum(item.total_price for item in cart_items)
    
    # Define additional charges (e.g., shipping cost)
    shipping_cost = 10  # Example fixed shipping cost
    
    # Calculate total
    total = subtotal + shipping_cost

    # Count cart items
    cart_count = Cart.objects.filter(user=request.user).count()
    
    # Pass the calculated values to the template
    return render(request, 'buyer_app/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
        'cart_count': cart_count
    })

@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    # Use request.user.user_type directly
    if request.user.user_type == 'buyer':  
        if request.method == "POST":
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                cart_item.delete()
        return redirect('cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    # Use request.user.user_type directly
    if request.user.user_type == 'buyer':  
        cart_item.delete()
    
    return redirect('cart')