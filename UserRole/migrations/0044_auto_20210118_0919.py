# Generated by Django 2.1.8 on 2021-01-18 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0043_auto_20201224_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='auth_user',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='company',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='profile',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
