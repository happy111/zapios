# Generated by Django 2.1.8 on 2020-02-28 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0006_company_is_sound'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_open',
            field=models.BooleanField(default=1, verbose_name='Is Open'),
        ),
    ]