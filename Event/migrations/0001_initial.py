# Generated by Django 2.1.8 on 2020-10-01 06:23

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Brands', '0012_company_plan_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=100, verbose_name='Event Name')),
                ('event_time', models.TimeField(blank=True, null=True, verbose_name='Event Time')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('is_key', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='HistoryEvent_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '    HistoryEvent',
                'verbose_name_plural': '  HistoryEvent',
            },
        ),
        migrations.CreateModel(
            name='PrimaryEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=100, verbose_name='Event Type')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='PrimaryEvent_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '    Event Type',
                'verbose_name_plural': '    Event Type',
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Trigger Type')),
                ('trigger_importance', models.CharField(blank=True, max_length=100, null=True, verbose_name='Trigger Type')),
                ('outlet', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Outlet Mapped Ids')),
                ('send', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Send')),
                ('to', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='To')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Trigger Content')),
                ('day', models.CharField(blank=True, max_length=100, null=True, verbose_name='Trigger day')),
                ('event_time', models.TimeField(blank=True, null=True, verbose_name='Event Time')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Trigger_Company', to='Brands.Company', verbose_name='Company')),
                ('trigger_name', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Trigger_trigger_name', to='Event.PrimaryEventType', verbose_name='Trigger name')),
            ],
            options={
                'verbose_name': '    Trigger',
                'verbose_name_plural': '  Trigger',
            },
        ),
    ]