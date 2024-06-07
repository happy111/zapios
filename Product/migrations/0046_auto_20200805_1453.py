# Generated by Django 2.1.8 on 2020-08-05 09:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0045_auto_20200805_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='secondary_ingredient',
        ),
        migrations.AddField(
            model_name='product',
            name='secondary_ingredients',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
