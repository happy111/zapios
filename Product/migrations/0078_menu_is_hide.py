# Generated by Django 2.1.8 on 2021-06-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0077_productsubcategory_is_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_hide',
            field=models.BooleanField(default=0, verbose_name='Is Active'),
        ),
    ]
