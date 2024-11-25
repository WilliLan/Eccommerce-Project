from django.contrib import admin
from .models import Seller_Summary, WithdrawalLog

# Create WithdrawalLog inline for Seller_Summary
class WithdrawalLogInline(admin.StackedInline):
    model = WithdrawalLog
    extra = 0  # No extra blank forms shown

# Define a custom admin class for Seller_Summary
class SellerAdmin(admin.ModelAdmin):
    model = Seller_Summary
    readonly_fields = []  # Add fields to make them read-only if needed
    inlines = [WithdrawalLogInline]  # Add the inline logs

# Register models with the admin site
admin.site.register(Seller_Summary, SellerAdmin)
admin.site.register(WithdrawalLog)
