# Generated by Django 2.1.8 on 2020-08-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0016_primaryingredient_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondaryingredient',
            name='is_primary',
            field=models.BooleanField(default=0, verbose_name='Is Primary'),
        ),
    ]
