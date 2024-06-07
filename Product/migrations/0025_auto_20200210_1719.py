# Generated by Django 2.1.8 on 2020-02-10 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0024_auto_20200210_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featureproduct',
            name='outlet',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='Outlet.OutletProfile', verbose_name='Outlet'),
        ),
    ]