# Generated by Django 2.1.8 on 2020-09-04 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0050_auto_20200902_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pvideo',
            field=models.FileField(blank=True, null=True, upload_to='video/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='food_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.FoodType', verbose_name='Product Type'),
        ),
    ]