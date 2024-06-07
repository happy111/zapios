# Generated by Django 2.1.8 on 2019-11-03 17:32

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Brands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddonDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addon_gr_name', models.CharField(max_length=50, verbose_name='Addon Group Name')),
                ('min_addons', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Minimum No. of Add-Ons')),
                ('max_addons', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Maximum No. of Add-Ons')),
                ('associated_addons', django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                ('active_status', models.BooleanField(blank=True, default=1, null=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
            ],
            options={
                'verbose_name': 'Add-on Group',
                'verbose_name_plural': '         Add-on Groups',
            },
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(max_length=50, unique=True, verbose_name='Food Type Name')),
                ('foodtype_image', models.ImageField(blank=True, null=True, upload_to='foodtype_images/images', verbose_name='Image (Short image)')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
            ],
            options={
                'verbose_name': 'Food Type',
                'verbose_name_plural': '            Food Type',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='Product Name')),
                ('priority', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)], verbose_name='Priority')),
                ('product_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Product Code')),
                ('product_desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='Product Description')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product_image/', verbose_name='Image')),
                ('outlet_map', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('variant_deatils', django.contrib.postgres.fields.jsonb.JSONField()),
                ('addpn_grp_association', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('food_type', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, to='Product.FoodType', verbose_name='Product Type')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': '       Products',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True, verbose_name='Category Name')),
                ('category_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Category Code')),
                ('outlet_map', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None, verbose_name='Outlet Mapped Ids')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('priority', models.PositiveIntegerField(blank=True, null=True, verbose_name='Priority')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='category_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': '             Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductsubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=50, verbose_name='Subcategory Name')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('category', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Products_subcategory', to='Product.ProductCategory', verbose_name='Category Name')),
            ],
            options={
                'verbose_name': '   Sub-Category',
                'verbose_name_plural': '             Sub-Categories',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=130, verbose_name='Variant Measurement')),
                ('description', models.CharField(blank=True, max_length=110, null=True, verbose_name='Description')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('Company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Variant_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Variant',
                'verbose_name_plural': '          Variants',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='Product_Category', to='Product.ProductCategory', verbose_name='Product Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_subcategory',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_subCategory', to='Product.ProductsubCategory', verbose_name='Product Sub Category'),
        ),
        migrations.AddField(
            model_name='addondetails',
            name='product_variant',
            field=models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, to='Product.Variant', verbose_name='Variant'),
        ),
    ]
