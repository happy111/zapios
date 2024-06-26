# Generated by Django 2.1.8 on 2021-04-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0062_outletprofile_delivery_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='landmark',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='outletprofile',
            name='pincode',
            field=models.CharField(default=1, max_length=50, verbose_name='Pincode'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outletprofile',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='city'),
        ),
    ]
