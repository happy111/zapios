# Generated by Django 2.1.8 on 2020-03-14 08:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0010_auto_20200220_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='outlet_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), blank=True, null=True, size=None),
        ),
    ]
