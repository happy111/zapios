# Generated by Django 2.1.8 on 2020-02-05 07:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0006_company_is_sound'),
        ('Product', '0021_product_discount_price'),
        ('discount', '0008_auto_20191217_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='PercentOffers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Offer Name')),
                ('discount_percent', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Discount Percentage')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('category', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='PercentOffer_Category', to='Product.ProductCategory', verbose_name='Category')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='PercentOffer_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'PercentageOffer',
                'verbose_name_plural': ' PercentageOffer',
            },
        ),
    ]