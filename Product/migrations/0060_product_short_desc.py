# Generated by Django 2.1.8 on 2020-10-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0059_auto_20201014_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_desc',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Short Description'),
        ),
    ]
