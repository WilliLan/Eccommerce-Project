# Generated by Django 5.1.2 on 2024-10-31 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyerStore', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address1',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
