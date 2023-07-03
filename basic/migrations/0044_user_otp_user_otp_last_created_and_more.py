# Generated by Django 4.1.4 on 2023-07-02 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0043_remove_order_area_remove_order_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_last_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 2, 9, 57, 35, 26859)),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='delivary_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 7, 2)),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(max_length=20),
        ),
    ]