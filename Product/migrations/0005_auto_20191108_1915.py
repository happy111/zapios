# Generated by Django 2.1.8 on 2019-11-08 13:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_auto_20191108_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variant_deatils',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True),
        ),
    ]
