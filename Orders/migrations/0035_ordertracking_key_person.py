# Generated by Django 2.1.8 on 2020-04-23 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0034_order_synced'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertracking',
            name='key_person',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Key Person'),
        ),
    ]