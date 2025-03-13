from django.urls import path
from . import views

urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_menu/', views.seller_menu, name='seller_menu'),
    path('add/', views.add_product, name='add_product'),
    path('<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.menu_detail, name='menu_detail'),


   # path('category/',views.category,name='category'),      #read
    path('create/', views.category_create, name='category_create'),    # Create
    path('<int:id>/update/', views.category_update, name='category_update'),  # Update
    path('<int:id>/delete/', views.category_delete, name='category_delete'),  #delete  
    path('logout/',views.seller_logout,name='seller_logout'),

    path('cart/', views.view_cart, name='cart'),  # View cart items
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),  # Update quantity in cart
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove product from cart
]
