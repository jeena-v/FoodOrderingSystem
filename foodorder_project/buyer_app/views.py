from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login
#from .forms import RegisterForm,LoginForm
from .forms import BuyerRegisterForm, SellerRegisterForm,LoginForm
from seller_app.models import Product,Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful as a Buyer!")
            return redirect('buyer_dashboard')
    else:
        form = BuyerRegisterForm()

    return render(request, 'buyer_app/buyer_register.html', {'form': form})

# View for Seller Registration
def seller_register(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful as a Seller!")
            return redirect('seller_dashboard')
    else:
        form = SellerRegisterForm()

    return render(request, 'buyer_app/seller_register.html', {'form': form})
from django.shortcuts import render
from buyer_app.models import CustomUser  # Adjust import as per your app structure




@login_required
def buyer_dashboard(request):
    if request.user.user_type == 'seller':
        return redirect('seller_dashboard')
    elif request.user.user_type == 'buyer':
        products = Product.objects.all()
        sellers = CustomUser.objects.filter(user_type='seller')  # Fetch sellers
        return render(request, 'buyer_app/buyer_dashboard.html',{'products':products,'sellers': sellers})
    return render(request, 'foodorder_app/index.html')


from django.shortcuts import get_object_or_404

@login_required
def seller_products(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller')  # Use user_type instead of is_seller
    products = Product.objects.filter(seller=seller)  # Fetch products of this seller
    return render(request, 'buyer_app/seller_products.html', {'seller': seller, 'products': products})



@login_required
def buyer_menu(request):
    if request.user.user_type != 'buyer':
        return HttpResponseForbidden("You are not authorized to view this page")
    
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'buyer_app/buyer_menu.html', {'products': products,'categories':categories})
from django.shortcuts import render, get_object_or_404
# Product Detail View
@login_required
def product_detail(request, product_id):
    # Get the product by ID or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Render the product details page with the product information
    return render(request, 'buyer_app/product_detail.html', {'product': product})





def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                auth_login(request, user)

                # Check if the user is a seller or buyer
                if user.user_type == 'seller':
                    return redirect("seller_dashboard")  # Redirect to seller's dashboard
                elif user.user_type == 'buyer':
                    return redirect("buyer_dashboard")  # Redirect to buyer's dashboard
                else:
                    return redirect("index")  # Default redirect if user_type is neither

            else:
                messages.error(request, "Invalid username or password")
    
    return render(request,"buyer_app/login.html", {"form": form})



from django.shortcuts import redirect
from django.contrib.auth import logout

def buyer_logout(request):
    # Log out the user
    logout(request)
    # Redirect to the home page or login page after logging out
    return redirect('index')  

#def online_order(request):
 #   return render(request, 'buyer_app/online_order.html')


