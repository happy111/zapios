# Generated by Django 2.1.8 on 2020-07-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0040_auto_20200706_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='primary_image',
            field=models.BooleanField(default=0, verbose_name='Primary Image'),
        ),
    ]