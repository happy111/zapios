# Generated by Django 2.1.8 on 2020-03-30 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0020_auto_20200330_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rollpermission',
            name='route',
        ),
        migrations.RemoveField(
            model_name='rollpermission',
            name='sub_route',
        ),
    ]
