# Generated by Django 2.1.8 on 2021-01-07 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0060_auto_20201204_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='radius',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Time Range'),
        ),
    ]
