# Generated by Django 2.1.8 on 2021-06-17 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0036_company_billing_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='billing_currency',
        ),
    ]
