from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('buyerStore.urls')), # buyerStore represents buyerStore app, urls represents the urls.py in buyerStore
    path('cart/', include('cart.urls')),
    path('buyerCheckout/', include('buyerCheckout.urls')),
    path('sellerDashboard/', include('sellerDashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # allow us to upload images
