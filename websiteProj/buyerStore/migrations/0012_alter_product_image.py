# Generated by Django 5.1.2 on 2024-12-04 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyerStore', '0011_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(max_length=1000),
        ),
    ]
