# Generated by Django 2.1.8 on 2021-01-18 03:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0071_auto_20210113_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='package_tax',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Package Tax Ids'),
        ),
    ]
