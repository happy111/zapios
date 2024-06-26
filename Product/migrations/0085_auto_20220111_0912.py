# Generated by Django 2.1.8 on 2022-01-11 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0084_auto_20220111_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addons',
            name='Company',
        ),
        migrations.AlterField(
            model_name='addons',
            name='addon_amount',
            field=models.FloatField(default=1, verbose_name='Add-On Amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addons',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Add-On Name'),
        ),
    ]
