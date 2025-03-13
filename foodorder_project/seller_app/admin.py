from django.contrib import admin
from .models import Product,Category

# Register your models here.
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')  # Columns to display
    list_filter = ('user_type',)  # Add filter options by 'user_type'
    search_fields = ('username', 'email')  # Allow searching by username or email

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Category)