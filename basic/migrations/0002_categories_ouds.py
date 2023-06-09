# Generated by Django 4.1.4 on 2022-12-25 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='No Categories', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ouds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('type', models.CharField(default='open', max_length=5)),
                ('description', models.CharField(max_length=1000)),
                ('base_price', models.DecimalField(decimal_places=2, default='000000.00', max_digits=30)),
                ('amount', models.DecimalField(decimal_places=2, default='0000.00', max_digits=10)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('cover_image1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('cover_image2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('cover_image3', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.categories')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
