# Generated by Django 2.1.8 on 2020-10-15 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0004_citymaster_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citymaster',
            name='state',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_master_city', to='Location.StateMaster', verbose_name='State'),
        ),
    ]
