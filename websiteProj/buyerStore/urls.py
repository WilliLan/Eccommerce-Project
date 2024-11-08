from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('update_info/', views.update_info, name='update_info'),
    path('search/', views.product_search, name='product_search'),
    path('order_history/', views.order_history, name='order_history'),
]


