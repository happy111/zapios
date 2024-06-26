# Generated by Django 2.1.8 on 2021-06-14 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0032_mergebrand'),
        ('Location', '0038_auto_20210614_1722'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='areamaster',
        #     name='company',
        #     field=models.ForeignKey(default=1, limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='area_Company', to='Brands.Company', verbose_name='Company'),
        #     preserve_default=False,
        # ),
        migrations.AlterField(
            model_name='countrymaster',
            name='country',
            field=models.CharField(max_length=200, unique=True, verbose_name='Country'),
        ),
    ]
