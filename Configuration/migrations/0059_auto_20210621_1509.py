# Generated by Django 2.1.8 on 2021-06-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0058_onlinepaymentstatus_is_hide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinepaymentstatus',
            name='types',
            field=models.CharField(choices=[('delivery', 'delivery'), ('pickup', 'pickup')], max_length=50, verbose_name='Type'),
        ),
    ]
