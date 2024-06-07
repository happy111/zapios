# Generated by Django 2.1.8 on 2022-01-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0071_auto_20211128_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletprofile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='state',
        ),
        migrations.AddField(
            model_name='outletprofile',
            name='prefecture',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Prefecture'),
        ),
        migrations.AlterField(
            model_name='outletprofile',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Address'),
        ),
    ]
