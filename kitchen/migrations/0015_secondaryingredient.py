# Generated by Django 2.1.8 on 2020-07-28 02:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0009_auto_20200720_1327'),
        ('kitchen', '0014_primaryingredient_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondaryIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='PrimaryIngredient name')),
                ('primary_deatils', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='SecondaryIngredient_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'SecondaryIngredient',
                'verbose_name_plural': ' SecondaryIngredient',
            },
        ),
    ]
