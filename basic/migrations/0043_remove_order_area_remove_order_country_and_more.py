# Generated by Django 4.1.4 on 2023-07-01 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0042_userorder_order_date_alter_tracker_delivary_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='area',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='town',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='area',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='country',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='town',
        ),
    ]