# Generated by Django 2.1.8 on 2021-01-12 05:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0061_outletprofile_radius'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='delivery_zone',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
