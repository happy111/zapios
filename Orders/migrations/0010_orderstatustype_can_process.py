# Generated by Django 2.1.8 on 2020-01-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0009_order_is_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatustype',
            name='can_process',
            field=models.BooleanField(default=1, verbose_name='Can Process'),
        ),
    ]