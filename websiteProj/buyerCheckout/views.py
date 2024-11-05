from django.shortcuts import render

def payment_success(request):
    return render(request, 'buyerCheckout/payment_success.html', {})
