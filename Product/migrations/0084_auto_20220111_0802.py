# Generated by Django 2.1.8 on 2022-01-11 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0083_auto_20220111_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addons',
            name='is_hide',
        ),
        migrations.RemoveField(
            model_name='addons',
            name='priority',
        ),
    ]