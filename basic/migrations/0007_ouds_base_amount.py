# Generated by Django 4.1.4 on 2023-01-02 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='ouds',
            name='base_amount',
            field=models.DecimalField(decimal_places=2, default='2.5', max_digits=10),
        ),
    ]
