# Generated by Django 2.1.8 on 2020-11-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0018_auto_20201109_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='active_status',
            field=models.BooleanField(default=1, verbose_name='Is Active'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='is_promotions',
            field=models.BooleanField(default=0, verbose_name='Is Promotions'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Updation Date'),
        ),
    ]
