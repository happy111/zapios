# Generated by Django 2.1.8 on 2022-01-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0050_order_schedule_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(blank=True, max_length=1500, null=True, verbose_name='Note'),
        ),
    ]