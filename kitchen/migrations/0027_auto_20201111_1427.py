# Generated by Django 2.1.8 on 2020-11-11 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0026_recipeingredient_output_yield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='primaryingredient',
            name='company',
        ),
        migrations.RemoveField(
            model_name='primaryingredient',
            name='food_type',
        ),
        migrations.RemoveField(
            model_name='secondaryingredient',
            name='company',
        ),
        migrations.RemoveField(
            model_name='secondaryingredient',
            name='primary_ingredient',
        ),
        migrations.DeleteModel(
            name='PrimaryIngredient',
        ),
        migrations.DeleteModel(
            name='SecondaryIngredient',
        ),
    ]