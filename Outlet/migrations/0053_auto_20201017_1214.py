# Generated by Django 2.1.8 on 2020-10-17 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0052_auto_20201016_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletprofile',
            name='auth_user',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='mobile_with_isd',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='user_type',
        ),
    ]
