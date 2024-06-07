# Generated by Django 2.1.8 on 2019-12-09 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0005_company_company_landing_imge'),
        ('Outlet', '0005_auto_20191128_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletmilesrules',
            name='Outlet',
        ),
        migrations.AddField(
            model_name='outletmilesrules',
            name='Company',
            field=models.ForeignKey(default=1, limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='OutletMilesRules_Company', to='Brands.Company', verbose_name='Company'),
            preserve_default=False,
        ),
    ]