from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from buyerCheckout.models import OrderItem
from decimal import Decimal, ROUND_HALF_UP
from django.utils.timezone import now

class Seller_Summary(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    revenue = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Total revenue generated from all orders
    total_orders = models.IntegerField(default=0)  # Total number of orders
    total_balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Seller's current balance
    withdrawals = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Total amount withdrawn

    def __str__(self):
        return f"Seller Summary for {self.seller}"

    def update_revenue_and_balance(self):
        """
        Update revenue and total orders from completed orders.
        Does not overwrite `total_balance`—instead, adjusts it by subtracting withdrawals.
        """
        completed_order_items = OrderItem.objects.filter(
            product__seller=self.seller,
            order__paid=True,  # Only consider orders that are paid
        )

        total_revenue = completed_order_items.aggregate(Sum('price'))['price__sum'] or 0
        total_orders = completed_order_items.count()

        total_revenue = Decimal(total_revenue).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        total_balance = total_revenue - self.withdrawals

        self.revenue = total_revenue
        self.total_orders = total_orders
        self.total_balance = Decimal(total_balance).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.save()

    def update_balance(self, amount):
        """
        Update the seller's total balance. Positive amount adds, negative deducts.
        """
        self.total_balance += amount
        self.save()

    def record_withdrawal(self, amount):
        """
        Deduct a withdrawal amount, update withdrawals total, and log the transaction.
        """
        self.withdrawals += Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.update_balance(-amount)
        WithdrawalLog.objects.create(seller_summary=self, amount=amount)


class WithdrawalLog(models.Model):
    seller_summary = models.ForeignKey(Seller_Summary, on_delete=models.CASCADE, related_name="withdrawal_logs")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(default=now)  # Automatically logs the date and time of withdrawal
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f"Withdrawal of ${self.amount} on {self.date.strftime('%Y-%m-%d %H:%M:%S')} by {self.seller_summary.seller} wid:{self.id}"
    