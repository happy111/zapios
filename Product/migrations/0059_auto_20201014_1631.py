# Generated by Django 2.1.8 on 2020-10-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0058_auto_20201014_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_image',
            field=models.FileField(default=1, upload_to='menu_image/', verbose_name='Image'),
            preserve_default=False,
        ),
    ]
