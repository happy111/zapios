# Generated by Django 2.1.8 on 2020-10-14 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0055_product_packing_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=100, verbose_name='Menu Name')),
                ('menu_image', models.ImageField(blank=True, null=True, upload_to='menu_image/', verbose_name='Image')),
                ('active_status', models.BooleanField(default=1, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': '       Menu',
            },
        ),
    ]
