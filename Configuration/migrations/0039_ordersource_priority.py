# Generated by Django 2.1.8 on 2020-11-10 06:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0038_auto_20201109_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersource',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Priority'),
        ),
    ]