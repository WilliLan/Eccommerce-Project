from django.shortcuts import render, get_object_or_404 # getting object or return 404 error msg
from . cart import Cart # Cart Class
from buyerStore.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})


def cart_add(request):
    # Get cart
    cart = Cart(request)
    
    # Test for POST
    if request.POST.get('action') == 'post': # JS block in product.html

        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id) # (Product table, lookup id)

        # Save to Session
        cart.add(product=product, quantity=product_qty)
        
        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, f"{product.name} added to cart")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post': # JS block in cart_summary.html 'action'
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, "Item Deleted From Cart")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post': # JS block in cart_summary.html 'action'

        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, "Cart Updated")
        return response
        # return redirect('cart_summary')

def checkout(request):
    return render(request, "checkout.html")