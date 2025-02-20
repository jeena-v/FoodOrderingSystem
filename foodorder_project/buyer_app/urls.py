from django.urls import path
from . import views

urlpatterns = [
            #path('', views.home, name='home'),

    path("login/", views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('register/buyer/', views.buyer_register, name='buyer_register'),
    path('register/seller/', views.seller_register, name='seller_register'),
]
