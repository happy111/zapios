# Generated by Django 2.1.8 on 2021-01-09 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0048_auto_20201222_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='day',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Day'),
        ),
    ]
