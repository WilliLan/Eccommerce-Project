from django.urls import path
from . import views

urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('order/<int:order_item_id>/', views.order_detail, name='order_detail'),
    path('update-order-status/<int:order_item_id>/', views.update_order_status, name='update_order_status'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('withdraw_history', views.withdraw_history, name='withdraw_history'),
]
