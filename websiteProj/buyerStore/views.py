from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout # Login, Logout Authentication
from django.contrib import messages
from . forms import SignUpForm, UserInfoForm
import json
from buyerCheckout.models import Order, OrderItem
from cart.cart import Cart # from folder cart -> cart.py -> class Cart
from django.core.paginator import Paginator
from sellerDashboard.models import Seller_Summary

def category(request, foo): # foo = category name
    # replace hyphens with spaces
    foo = foo.replace('-', ' ')

    try:
        # Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
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
                products = Product.objects.filter(category=category, is_sale=True)
                if not products:
                    messages.error(request, "No Items on Sale")
                    return redirect('category', foo=foo)
                
        
        return render(request, 'category.html', {'products':products, 'category':category, 'filter_option': filter_option})
    except:
        messages.error(request, ("That Category Does Not Exist"))
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
                if profile.approved and Seller_Summary.objects.filter(seller=user).exists():
                    return redirect('seller_dashboard')
                elif profile.approved:
                    Seller_Summary.objects.create(
                    seller=user,
                    revenue=0,
                    total_orders=0,
                    total_balance=0,
                    withdrawals=0
                    )
                    return redirect('seller_dashboard')  # Redirect after creating the summary
                else:
                    logout(request)
                    messages.error(request, "Your account is not approved yet. Please wait for an Admin to approve your account.")
                    return redirect('home')
            else:  # admin
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
            messages.error(request, "You are not allowed to view this page")
            return redirect('home')

        orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Order by recent

        # Implement pagination (5 orders per page)
        paginator = Paginator(orders, 5)
        page_number = request.GET.get('page')  # Get the current page number from query params
        page_obj = paginator.get_page(page_number)  # Get the current page

        # Calculate the first and last page, and pages to show for pagination
        
        first_page = 1
        last_page = paginator.num_pages
        pages_to_show = range(max(1, page_obj.number - 2), min(page_obj.number + 3, last_page + 1))

        return render(request, 'order_history.html', {
            'orders': page_obj,
            'first_page': first_page,
            'last_page': last_page,
            'pages_to_show': pages_to_show,
            'page_obj': page_obj,
        })
    else:
        return redirect('login')
    
def compare(request, foo):
    # Get all available products for the dropdown
    foo = foo.replace('-', ' ')
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
    
    # Default to None if no comparison products are selected
    compare_products = None

    # Handle form submission to compare products
    if request.GET.get('compare1') and request.GET.get('compare2'):
        if request.GET['compare1'] == request.GET['compare2']:
            messages.error(request, "Please Choose Two Different Products To Compare!")
            # Return to the template with the error message and the same category/products
            return render(request, 'compare.html', {
                'products': products,
                'category': category,
                'compare_products': compare_products
            })
    
        # Get the two selected products
        product1 = Product.objects.get(id=request.GET['compare1'])
        product2 = Product.objects.get(id=request.GET['compare2'])
        compare_products = [product1, product2]

    return render(request, 'compare.html', {
        'products': products,       # List of all products for dropdown
        'compare_products': compare_products,  # List of products to compare
        'category': category,
    })

def buyer_order_details(request, order_id):
    if request.user.is_authenticated:
        if request.user.profile.account_type == 'seller':
            messages.error(request, "You are not allowed to view this page")
            return redirect('home')

        # Get the order object and related order items
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        # Prepare the order details
        order_info = {
            'fullname': order.full_name,
            'address': f"{order.address1 or ''} {order.address2 or ''}".strip(),
            'city': order.city,
            'state': order.state,
            'zipcode': order.zipcode,
            'created_at': order.created_at,
        }

        # Group order items by seller
        seller_products = {}
        total_items = 0
        
        for order_item in order_items:
            seller = order_item.product.seller
            if seller not in seller_products:
                seller_products[seller] = []
            seller_products[seller].append(order_item)
            total_items += order_item.quantity
            

        # Pass the data to the template
        return render(request, 'buyer_order_details.html', {
            'order_id': order.id,
            'order_info': order_info,
            'order_items': order_items,
            'seller_products': seller_products,
            'total_items': total_items,
            
            
        })
    else:
        messages.error(request, "You must be Logged in.")
        return redirect('home')
    
def contact(request):
    return render(request, 'contact.html')
