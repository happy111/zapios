# Generated by Django 2.1.8 on 2020-03-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0016_auto_20200318_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='is_all_product',
            field=models.BooleanField(blank=True, default=1, null=True, verbose_name='Is All Product'),
        ),
    ]