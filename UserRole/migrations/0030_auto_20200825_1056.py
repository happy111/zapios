# Generated by Django 2.1.8 on 2020-08-25 05:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0029_auto_20200804_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerprofile',
            name='login_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Login Type'),
        ),
    ]
