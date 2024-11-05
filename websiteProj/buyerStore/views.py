from django.shortcuts import render, redirect
from . models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout # Login, Logout Authentication
from django.contrib import messages
from django.contrib.auth.models import User # Register new user
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm, UserInfoForm
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
            try: # Check if user has a profile - for admin (no profile)
                profile = Profile.objects.get(user=user)
                account_type = profile.account_type

                # Redirect based on account type
                if account_type == 'buyer':
                    return redirect('home')  
                elif account_type == 'seller':
                    return redirect('about')  
                
            except Profile.DoesNotExist: # for admin (no profile)
                    return redirect('http://127.0.0.1:8000/admin')  # edit redirect after hosted on web
        
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
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # login in user
            user=authenticate(username=username, password=password)
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