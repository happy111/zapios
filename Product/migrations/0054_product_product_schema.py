# Generated by Django 2.1.8 on 2020-10-05 06:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0053_auto_20200909_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]