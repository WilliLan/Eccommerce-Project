from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout # Login, Logout Authentication
from django.contrib import messages
from django.contrib.auth.models import User # Register new user
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm, UserInfoForm
from django import forms
import json
from buyerCheckout.models import Order, OrderItem
from cart.cart import Cart # from folder cart -> cart.py -> class Cart


def category(request, foo): # foo = category name
    # replace hyphens with spaces
    foo = foo.replace('-', ' ')

    try:
        # Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That Category Does Not Exist"))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    filter_option = None
    if request.method == "POST":
        filter_option = request.POST.get('filter')
        if filter_option == "option1":  # Price: Low to High
            
            products = sorted(
                products,
                key=lambda p: p.sale_price if p.is_sale else p.price
            )
        elif filter_option == "option2":  # Price: High to Low
            
            products = sorted(
                products,
                key=lambda p: p.sale_price if p.is_sale else p.price,
                reverse=True
            )
        elif filter_option == "option3":  # On Sale
            products = Product.objects.filter(is_sale=True)
    
    return render(request, 'home.html', {'products':products, 'filter_option':filter_option})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    # Check to see if submit was clicked on login page
    if request.method == "POST":
        # Take in value from form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate using django auth
        user = authenticate(request, username=username, password=password)

        # Successful Login
        if user is not None:
            login(request, user)
            # Check if user has a profile
            profile = Profile.objects.get(user=user)
            account_type = profile.account_type

            # Redirect based on account type
            if account_type == 'buyer':
                current_user = Profile.objects.get(user__id=request.user.id)
                # Get their saved cart from db
                saved_cart = current_user.old_cart
                if saved_cart:
                    try:
                        # Convert string cart to dictionary using JSON
                        converted_cart = json.loads(saved_cart)
                        # Add the loaded cart dictionary to the session cart
                        cart = Cart(request)
                        # Loop through the cart and add the items from the dictionary
                        for key, value in converted_cart.items():
                            cart.db_add(product_id=key, quantity=value)
                    except json.JSONDecodeError:
                        pass
                return redirect('home')
            
            elif account_type == 'seller':
                if profile.approved == True:
                    return redirect('seller_dashboard') 
                else:
                    logout(request)
                    messages.error(request, ("Your account is not approved yet. Please wait for an Admin to approve your account."))
                    return redirect('home')
            else: # admin
                return redirect('home')

            
        
        # Failed to login
        else:
            messages.error(request, ("Either your email or password was incorrect. Try again please!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST) # Take all info they put on the signup form and put into backend
        acc_type = form.data['account_type']

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            
            user=authenticate(username=username, password=password)
            
            if acc_type == 'seller':
                user.profile.approved = False
                user.profile.save()
                messages.success(request, ("Admin will review this request. You will be notified status via email."))
                return redirect('home')

            elif acc_type == 'buyer':
                login(request, user)
                messages.success(request, ("You Have Registered Successfully - Please Fill Out Your Information Below"))
                return redirect('update_info')
        
        else:
            messages.error(request, ("Requirement(s) was violated, Please read carefully and Try again!"))
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'form':form})
    
def update_info(request):
    if request.user.is_authenticated:
        if request.user.profile.account_type == 'seller':
            messages.error(request, ("You are not allowed to view this page"))
            return redirect('home')
        try:
            current_user = Profile.objects.get(user__id=request.user.id)
            form = UserInfoForm(request.POST or None, instance=current_user)
            if form.is_valid():
                form.save()
                messages.success(request, ("Your Information Has Been Updated"))
                return redirect('home')
            return render(request, 'update_info.html', {'form':form})
        except Profile.DoesNotExist:
            messages.error(request, ("You can't update your information"))
            return redirect('home')
    else:
        messages.error(request, ("Please Login to Update Your Information"))
        return redirect('login')
    
def product_search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    return render(request, 'product_search.html', {'products': products, 'query': query})

def order_history(request):
    if request.user.is_authenticated:
        if request.user.profile.account_type == 'seller':
            messages.error(request, ("You are not allowed to view this page"))
            return redirect('home')
        try:

            orders = Order.objects.filter(user__id=request.user.id)
            
            print(orders)
            return render(request, 'order_history.html', {'orders': orders})
        except Order.DoesNotExist:
            #return render(request, 'order_history.html', {})
            pass

    else:
        messages.error(request, ("Please Login to View Your Order History"))
        return redirect('login')
"""
def order_details(request, pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})
"""


    