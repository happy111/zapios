# Generated by Django 2.1.8 on 2020-08-31 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0021_paymentmethod_word_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=250, null=True)),
                ('is_success', models.BooleanField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updation Date & Time')),
            ],
        ),
    ]
