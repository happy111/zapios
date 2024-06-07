# Generated by Django 2.1.8 on 2020-08-13 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0017_secondaryingredient_is_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondaryingredient',
            name='primary_ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SecondaryIngredient_primary_ingredient', to='kitchen.PrimaryIngredient', verbose_name='Primary Ingredient'),
        ),
    ]