# Generated by Django 4.2.4 on 2023-09-27 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0002_remove_inventory_userinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='last_sales_date',
            field=models.DateField(auto_now=True),
        ),
    ]