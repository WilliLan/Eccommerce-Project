from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from buyerStore.models import Profile, Product
from django.http import JsonResponse
from django.contrib import messages
from buyerCheckout.forms import PaymentForm

def checkout(request):
    
    cart = request.session.get('cart', {})
    cart = Cart(request)

    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    # Initialize profile data
    profile_data = {}

    if cart.cart_total() == 0:
        return redirect('cart_summary')

    if request.user.is_authenticated:
        
        try:
            profile = Profile.objects.get(user=request.user)
            profile_data = {
                'full_name': request.user.get_full_name(),
                'address1': profile.address1,
                'address2': profile.address2,
                'city': profile.city,
                'state': profile.state,
                'zipcode': profile.zipcode,
                'phone': profile.phone,
                'email': request.user.email,
            }
        except Profile.DoesNotExist:
            pass  # No profile exists, so leave profile_data empty

    if request.method == "POST":
        # Retrieve shipping info from POST data
        full_name = request.POST.get('full_name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create the Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zipcode=zipcode,
            total=totals,
        )
        # Create OrderItem for each product and quantity
        for key, value in quantities.items():
            for product in cart_products:
                if product.id == int(key):
                    price = product.sale_price if product.is_sale else product.price
                    OrderItem.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    order=order,
                    product=product,
                    quantity=value,
                    price=price*value,
                    )

        # Redirect to the payment success page
        if request.user.is_authenticated:
            cart.clear()
            for key in list(request.session.keys()):
                if key == 'cart_session_key':
                    del request.session[key]
        else:
            request.session.flush()
        Order.paid = True
        Order.save()
        return render(request, 'buyerCheckout/payment_success.html', {'order_id': order.id, 'totals': order.total, 'cart_products': cart_products, 'quantities': quantities})

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'profile_data': profile_data,
        'payment_form': PaymentForm(),
        
    }

    return render(request, 'buyerCheckout/checkout.html', context)

def payment_success(request):
    return render(request, 'buyerCheckout/payment_success.html', {})




