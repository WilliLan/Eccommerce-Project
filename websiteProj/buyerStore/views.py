from django.shortcuts import render, redirect
from . models import Product, Category
from django.contrib.auth import authenticate, login, logout # Login, Logout Authentication
from django.contrib import messages
from django.contrib.auth.models import User # Register new user
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm
from django import forms

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
    return render(request, 'home.html', {'products':products})

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
            messages.success(request, ("You Have Been Logged In"))
            return redirect('home')
        
        # Failed to login
        else:
            messages.success(request, ("Either your email or password was incorrect. Try again please!"))
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
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # login in user
            user=authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Registered Successfully"))
            return redirect('home')
        
        else:
            messages.success(request, ("Requirement(s) was violated, Please read carefully and Try again!"))
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'form':form})
    
