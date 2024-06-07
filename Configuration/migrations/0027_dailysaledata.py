# Generated by Django 2.1.8 on 2020-09-09 06:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0012_company_plan_name'),
        ('Configuration', '0026_merge_20200902_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySaledata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saledata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='saledata')),
                ('sale_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sale Name')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='DailySaledata_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '   DailySaledata',
                'verbose_name_plural': '   DailySaledata',
            },
        ),
    ]
