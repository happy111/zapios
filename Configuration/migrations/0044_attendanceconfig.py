# Generated by Django 2.1.8 on 2020-12-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0024_page_page'),
        ('Configuration', '0043_auto_20201205_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullday', models.TimeField()),
                ('halfday', models.TimeField()),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='AttendanceConfig', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '   Payment Credential',
                'verbose_name_plural': '   Payment Credential',
            },
        ),
    ]
