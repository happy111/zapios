# Generated by Django 2.1.8 on 2021-06-26 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0080_auto_20210626_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='video_url',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Video Url'),
        ),
    ]
