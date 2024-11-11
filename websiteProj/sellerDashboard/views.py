from django.shortcuts import render

def seller_dashboard(request):
    if request.user.profile.account_type == 'buyer':
            messages.error(request, ("You are not allowed to view this page"))
            return redirect('home')
    return render(request, 'seller_dashboard.html', {})