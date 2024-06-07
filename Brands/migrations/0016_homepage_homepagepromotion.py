# Generated by Django 2.1.8 on 2020-11-07 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brands', '0015_page_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hello_image_web', models.ImageField(blank=True, null=True, upload_to='webimage/', verbose_name='Hello Image For Web')),
                ('hello_image_mobile', models.ImageField(blank=True, null=True, upload_to='mobileimage/', verbose_name='Hello Image For Mobile')),
                ('carousel_text', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Carousel Text')),
                ('carousel_image', models.ImageField(blank=True, null=True, upload_to='carouselImage/', verbose_name='Carousel Image')),
                ('carousel_text1', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Carousel Text1')),
                ('carousel_image1', models.ImageField(blank=True, null=True, upload_to='carouselImage/', verbose_name='CarouselImage')),
                ('health_text', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Carousel Text1')),
                ('health_image', models.ImageField(blank=True, null=True, upload_to='HealthImage/', verbose_name='Health Image')),
                ('company', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='HomePage_Company', to='Brands.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Homepage',
                'verbose_name_plural': '        Homepage',
            },
        ),
        migrations.CreateModel(
            name='HomepagePromotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotions_image', models.ImageField(blank=True, null=True, upload_to='promotions/', verbose_name='Promotions Image')),
                ('homepage', models.ForeignKey(limit_choices_to={'active_status': '1'}, on_delete=django.db.models.deletion.CASCADE, related_name='HomepagePromotion_homepage', to='Brands.HomePage', verbose_name='Home Page')),
            ],
            options={
                'verbose_name': 'Homepage Promotions',
                'verbose_name_plural': '          Homepage Promotions',
            },
        ),
    ]
