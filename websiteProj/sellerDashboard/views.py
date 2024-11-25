
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from buyerStore.models import Product
from buyerStore.forms import ProductForm
from buyerCheckout.models import OrderItem, Order
from . models import Seller_Summary, WithdrawalLog
from decimal import Decimal, InvalidOperation
from django.db import transaction


def seller_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, ("You must be logged in as a seller to view your dashboard"))
        return redirect('login')    

    if request.user.profile.account_type == 'buyer':
        messages.error(request, ("You are not allowed to view this page"))
        return redirect('home')

    products = Product.objects.filter(seller=request.user)
    
    # Pagination setup: 3 products per page
    paginator = Paginator(products, 2)  # Show 2 products per page
    page_number = request.GET.get('page')  # Get the page number from URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    # Get the surrounding page numbers to display (4 pages total: 1 before, current, 2 after)
    page_range = list(page_obj.paginator.page_range)
    start_index = max(page_obj.number - 2, 1)  # Ensure it's not below 1
    end_index = min(page_obj.number + 2, page_obj.paginator.num_pages)  # Ensure it's not beyond the last page
    pages_to_show = page_range[start_index - 1:end_index]  # Slice the range for the pages to show

    orders = OrderItem.objects.filter(product__seller=request.user).order_by('-order__id')
    seller_summary = Seller_Summary.objects.get(seller=request.user)  
    seller_summary.update_revenue_and_balance()

    return render(request, 'seller_dashboard.html', {
        'page_obj': page_obj,  # Pass the page object to the template
        'pages_to_show': pages_to_show,  # Pass the pages to display
        'orders': orders,
        'seller_summary': seller_summary,
        'first_page': 1,  # Always show the first page
        'last_page': page_obj.paginator.num_pages,  # Always show the last page
    })

def add_product(request):
    if not hasattr(request.user, 'profile') or request.user.profile.account_type != 'seller':
        messages.error(request, "You don't have permission to add products.")
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                messages.success(request, 'Product added successfully!')
                return redirect('seller_dashboard')
            except Exception as e:
                print(f"Error saving product: {e}")
                messages.error(request, "An error occurred while saving the product.")
        else:
            print(form.errors)  # Debugging: Print form errors to the console
            messages.error(request, "Failed to add product. Please check the form.")
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

# Edit Product view

def edit_product(request, product_id):
    # Get the product or return a 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.seller:
        messages.error(request, 'You can not edit this product.')
        return redirect('home')
    # If the request method is POST, update the product
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Populate form with the existing product
        if form.is_valid():
            form.save()  # Save the updated product
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_dashboard')  # Redirect to seller dashboard
    else:
        form = ProductForm(instance=product)  # Pre-fill the form with the current product data

    # Render the edit product template
    return render(request, 'edit_product.html', {'form': form, 'product': product})

# Delete Product view

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.seller:
        messages.error(request, 'You can not delete this product.')
        return redirect('home')
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_dashboard')  # Redirect to the seller dashboard after deletion
    

    # Render a confirmation page before deleting
    return render(request, 'delete_product.html', {'product': product})
    
    

def order_detail(request, order_item_id):
    if not request.user.is_authenticated:
        messages.error(request, ("You must be logged in as a seller to view your dashboard"))
        return redirect('login')    

    if request.user.profile.account_type == 'buyer':
        messages.error(request, ("You are not allowed to view this page"))
        return redirect('home')
    # Get the order item and related order
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order = order_item.order  # Access the related order

    # Extract order details
    order_info = {
        'fullname': order.full_name,
        'address': f"{order.address1 or ''} {order.address2 or ''}".strip(),
        'city': order.city,
        'state': order.state,
        'zipcode': order.zipcode,
        'created_at': order.created_at
    }

    # Filter order items for this order and products belonging to the current seller
    order_items = OrderItem.objects.filter(order=order, product__seller=request.user)

    # Render the template with the order details
    return render(request, 'order_detail.html', {
        'order_id': order.id,
        'order_items': order_items,
        'order_info': order_info,
    })

# Update Order Status view (for marking order as shipped)

def update_order_status(request, order_item_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in as a seller to view your dashboard")
        return redirect('login')    

    if request.user.profile.account_type == 'buyer':
        messages.error(request, "You are not allowed to view this page")
        return redirect('home')
    
    # Get the order item and related order
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order = order_item.order  # Access the related order

    # Extract order details
    order_info = {
        'fullname': order.full_name,
        'address': f"{order.address1 or ''} {order.address2 or ''}".strip(),
        'city': order.city,
        'state': order.state,
        'zipcode': order.zipcode,
        'created_at': order.created_at
    }

    # Filter order items for this order and products belonging to the current seller
    order_items = OrderItem.objects.filter(order=order, product__seller=request.user)

    if request.method == 'POST':
        # Update shipment status and tracking number
        tracking_number = request.POST.get('tracking_number')  # Get the tracking number from the form
        if tracking_number:
            for order_item in order_items:
                order_item.seller_ship = True  # Mark the order item as shipped
                order_item.tracking_number = tracking_number  # Assign the tracking number
                order_item.save()  # Save each order item after updating

            messages.success(request, "Shipment confirmed and tracking number updated.")
        else:
            messages.error(request, "Please enter a tracking number.")

        return redirect('seller_dashboard')

    # Render the template with the order details
    return render(request, 'update_order_status.html', {
        'order_id': order.id,
        'order_items': order_items,
        'order_info': order_info,
    })

def withdraw(request):
    if not request.user.is_authenticated:
        messages.error(request, ("You must be logged in as a seller to view your dashboard"))
        return redirect('login')    

    if request.user.profile.account_type == 'buyer':
        messages.error(request, ("You are not allowed to view this page"))
        return redirect('home')
    
    # Retrieve seller summary safely
    try:
        seller = Seller_Summary.objects.get(seller=request.user)
    except Seller_Summary.DoesNotExist:
        messages.error(request, "Seller summary not found.")
        return redirect('seller_dashboard')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)  # Safely convert to Decimal
            if amount <= 0:
                messages.error(request, 'Please enter a valid withdrawal amount greater than 0.')
            elif amount > seller.total_balance:
                messages.error(request, 'Insufficient balance for this withdrawal.')
            else:
                
                seller.update_balance(-amount)
                seller.record_withdrawal(amount)
                seller.save()  # This will save the updated balance
                messages.success(request, f'Your withdraw of ${amount} has been submitted to be processed/reviewed.')
                return redirect('seller_dashboard')
        except (ValueError, InvalidOperation):
            messages.error(request, 'Please enter a valid withdrawal amount.')

    return render(request, 'withdraw.html', {
        'seller_summary': seller,
    })

def withdraw_history(request):
    if not request.user.is_authenticated:
        messages.error(request, ("You must be logged in as a seller to view your dashboard"))
        return redirect('login')    

    if request.user.profile.account_type == 'buyer':
        messages.error(request, ("You are not allowed to view this page"))
        return redirect('home')
    seller_summary = Seller_Summary.objects.get(seller=request.user)
    withdrawals = WithdrawalLog.objects.filter(seller_summary=seller_summary).order_by('-date')
    # Pagination
    paginator = Paginator(withdrawals, 5)  # Show 10 withdrawals per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the paginated page object

    return render(request, 'withdraw_history.html', {'page_obj': page_obj})
    