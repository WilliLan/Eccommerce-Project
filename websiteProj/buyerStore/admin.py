from django.contrib import admin
from django.contrib.auth.models import User
from . models import Category, Customer, Product, Profile
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
#admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]

admin.site.unregister(User) # Unregister the old way 
admin.site.register(User, UserAdmin) # Register the new way