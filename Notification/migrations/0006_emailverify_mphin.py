# Generated by Django 2.1.8 on 2021-03-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0005_auto_20210303_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverify',
            name='mphin',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Mphin'),
        ),
    ]
