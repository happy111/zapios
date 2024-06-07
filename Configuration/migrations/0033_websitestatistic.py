# Generated by Django 2.1.8 on 2020-10-23 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0013_company_subdomain'),
        ('Configuration', '0032_auto_20201008_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='No Of visitors')),
                ('visitors', models.CharField(blank=True, max_length=50, null=True, verbose_name='No Of visitors')),
                ('menu_views', models.CharField(blank=True, max_length=50, null=True, verbose_name='No Of Menu Views')),
                ('checkout', models.CharField(blank=True, max_length=50, null=True, verbose_name='checkout')),
                ('online_order', models.CharField(blank=True, max_length=50, null=True, verbose_name='Online Orders')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '    name',
                'verbose_name_plural': '    name',
            },
        ),
    ]