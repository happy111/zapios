# Generated by Django 2.1.8 on 2020-08-31 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0023_ordersource_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='excelimport',
            name='types',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Types'),
        ),
    ]