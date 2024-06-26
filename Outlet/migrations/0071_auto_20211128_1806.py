# Generated by Django 2.1.8 on 2021-11-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0070_auto_20210717_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='acceptance',
            field=models.CharField(default=1, max_length=100, verbose_name='Acceptance Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outletprofile',
            name='dispatch',
            field=models.CharField(default=1, max_length=100, verbose_name='Dispatch Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outletprofile',
            name='processing',
            field=models.CharField(default=1, max_length=100, verbose_name='Processing Time'),
            preserve_default=False,
        ),
    ]
