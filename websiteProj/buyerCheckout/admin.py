from django.contrib import admin
from .models import Order, OrderItem

# register the model with the admin site
admin.site.register(OrderItem)

# create OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
