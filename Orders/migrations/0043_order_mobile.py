# Generated by Django 2.1.8 on 2020-09-01 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0042_auto_20200827_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mobile',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='mobile'),
        ),
    ]
