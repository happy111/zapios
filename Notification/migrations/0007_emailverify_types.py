# Generated by Django 2.1.8 on 2021-04-20 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0006_emailverify_mphin'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverify',
            name='types',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='types'),
        ),
    ]