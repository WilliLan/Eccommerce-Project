# Generated by Django 5.1.2 on 2024-11-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyerStore', '0005_profile_address1_profile_address2_profile_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
