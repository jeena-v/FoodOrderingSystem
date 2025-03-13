
# Create your models here.
from django.db import models
from buyer_app.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField() 

    def __str__(self):
        return self.name  


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_pic/', blank=True, null=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories") 

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    


# New Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.product_name} (x{self.quantity})"

    @property
    def total_price(self):
        """Calculate total price for this cart item."""
        return self.quantity * self.product.price    



       


 
        
