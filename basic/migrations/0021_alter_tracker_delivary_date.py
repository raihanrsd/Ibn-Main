# Generated by Django 4.1.4 on 2023-05-13 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0020_alter_ouds_offer_status_alter_tracker_delivary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='delivary_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 5, 13)),
        ),
    ]
