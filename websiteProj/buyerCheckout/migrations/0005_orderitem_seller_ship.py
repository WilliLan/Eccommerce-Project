# Generated by Django 5.1.2 on 2024-11-25 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyerCheckout', '0004_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='seller_ship',
            field=models.BooleanField(default=False),
        ),
    ]
