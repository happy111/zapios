# Generated by Django 2.1.8 on 2020-11-02 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0064_menu_barcode_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='base_code',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='base code'),
        ),
    ]
