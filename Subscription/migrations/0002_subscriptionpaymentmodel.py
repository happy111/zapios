# Generated by Django 2.1.8 on 2020-09-02 11:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Subscription', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPaymentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=250, null=True)),
                ('key', models.CharField(blank=True, max_length=250, null=True)),
                ('secret', models.CharField(blank=True, max_length=250, null=True)),
                ('cost', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Subscription.SubscriptionPlanType')),
            ],
        ),
    ]
