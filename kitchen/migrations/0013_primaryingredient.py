# Generated by Django 2.1.8 on 2020-07-27 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0009_auto_20200720_1327'),
        ('Product', '0043_auto_20200717_1628'),
        ('kitchen', '0012_auto_20200303_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='PrimaryIngredient name')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='PrimaryIngredient_Company', to='Brands.Company', verbose_name='Company')),
                ('food_type', models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PrimaryIngredient_food', to='Product.FoodType', verbose_name='Food Type')),
            ],
            options={
                'verbose_name': 'PrimaryIngredient',
                'verbose_name_plural': ' PrimaryIngredient',
            },
        ),
    ]