from django.db import models
from django.contrib.auth.models import User
from buyerStore.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # User may be None
    full_name = models.CharField(max_length=255, blank=True)  # Will be filled during checkout
    email = models.EmailField(blank=True)  # Will be filled during checkout
    address1 = models.CharField(max_length=255, blank=True)  # Will be filled during checkout
    address2 = models.CharField(max_length=255, null=True, blank=True)  # Will be filled during checkout
    city = models.CharField(max_length=255, blank=True)  # Will be filled during checkout
    state = models.CharField(max_length=255, blank=True)  # Will be filled during checkout
    zipcode = models.CharField(max_length=255, blank=True)  # Will be filled during checkout
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Calculated during checkout
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-created when order is created
    shipped = models.BooleanField(default=False)  # Can be set later when order is shipped
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order - {str(self.id)}'

# Create OrderItem Model
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product ordered
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Price of the product

    def __str__(self):
        return f'OrderItem - {str(self.id)}'
