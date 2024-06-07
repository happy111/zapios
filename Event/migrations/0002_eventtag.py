# Generated by Django 2.1.8 on 2020-10-01 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0012_company_plan_name'),
        ('Event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100, verbose_name='Event Type')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='EventTag_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': '    Event Tag',
                'verbose_name_plural': '    Event Tag',
            },
        ),
    ]
