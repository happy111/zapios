# Generated by Django 2.1.8 on 2020-09-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0051_auto_20200904_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='kot_desc',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Kot Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='spice',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Spice'),
        ),
    ]
