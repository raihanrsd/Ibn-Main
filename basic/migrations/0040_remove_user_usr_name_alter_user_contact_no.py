# Generated by Django 4.1.4 on 2023-06-30 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0039_user_usr_name_alter_tracker_delivary_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='usr_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(default='01700000000', max_length=20, unique=True),
        ),
    ]