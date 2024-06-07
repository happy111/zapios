# Generated by Django 2.1.8 on 2020-09-15 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0045_order_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_delivery_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Customer Delivery Time'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_order_now',
            field=models.BooleanField(default=1, verbose_name='Is Order Now'),
        ),
    ]
