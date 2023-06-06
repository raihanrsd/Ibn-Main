# Generated by Django 4.1.4 on 2023-06-02 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0034_contactus_replied_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_shipping_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='delivary_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 6, 2)),
        ),
    ]
