# Generated by Django 2.1.8 on 2020-08-28 11:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0047_auto_20200806_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Priority'),
        ),
    ]
