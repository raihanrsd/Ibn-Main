# Generated by Django 4.1.4 on 2023-01-04 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_quantitymanagement_remove_ouds_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantitymanagement',
            old_name='amount1',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='amount2',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='amount3',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='amount4',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='amount5',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='name',
        ),
        migrations.RemoveField(
            model_name='quantitymanagement',
            name='number',
        ),
        migrations.RemoveField(
            model_name='ouds',
            name='amount_type',
        ),
        migrations.AddField(
            model_name='ouds',
            name='amount_type',
            field=models.ManyToManyField(to='basic.quantitymanagement'),
        ),
    ]
