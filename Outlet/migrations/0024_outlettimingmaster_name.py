# Generated by Django 2.1.8 on 2020-07-10 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0023_auto_20200710_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlettimingmaster',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='name'),
            preserve_default=False,
        ),
    ]
