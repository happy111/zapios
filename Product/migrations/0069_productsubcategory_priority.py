# Generated by Django 2.1.8 on 2020-11-30 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0068_auto_20201111_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsubcategory',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Priority'),
        ),
    ]