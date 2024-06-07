# Generated by Django 2.1.8 on 2020-03-17 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0007_company_is_open'),
        ('discount', '0012_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, max_length=100, null=True, verbose_name='Reason')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='DiscountReason_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Discount Reason',
                'verbose_name_plural': '   Discount Reason',
            },
        ),
    ]
