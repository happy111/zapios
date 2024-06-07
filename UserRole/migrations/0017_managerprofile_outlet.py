# Generated by Django 2.1.8 on 2020-03-19 18:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0016_auto_20200215_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerprofile',
            name='outlet',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Outlet Mapped Ids'),
        ),
    ]