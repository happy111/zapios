# Generated by Django 2.1.8 on 2021-01-07 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0025_company_attendance_type'),
        ('Location', '0032_areamaster_company'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='areamaster',
        #     name='company',
        #     field=models.ForeignKey(default=1, limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='area_Company', to='Brands.Company', verbose_name='Company'),
        #     preserve_default=False,
        # ),
    ]
