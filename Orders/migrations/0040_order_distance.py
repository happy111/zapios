# Generated by Django 2.1.8 on 2020-07-21 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0039_auto_20200516_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='distance',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Distance'),
        ),
    ]
