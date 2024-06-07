# Generated by Django 2.1.8 on 2021-07-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0069_auto_20210716_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='api_key',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='outletprofile',
            name='eion_outlet_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
