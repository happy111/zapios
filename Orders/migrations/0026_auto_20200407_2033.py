# Generated by Django 2.1.8 on 2020-04-07 15:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0025_auto_20200407_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='check_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Check List'),
        ),
    ]
