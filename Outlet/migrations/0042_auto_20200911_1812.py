# Generated by Django 2.1.8 on 2020-09-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0012_company_plan_name'),
        ('Outlet', '0041_auto_20200911_1812'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='outlettiming',
        #     name='slot',
        # ),
        # migrations.AddField(
        #     model_name='outletprofile',
        #     name='priority',
        #     field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Priority'),
        # ),
        migrations.AddField(
            model_name='outlettiming',
            name='slots',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='slots'),
        ),
        # migrations.AlterUniqueTogether(
        #     name='outletprofile',
        #     unique_together={('Company', 'priority')},
        # ),
    ]
