# Generated by Django 2.1.8 on 2021-03-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0002_emailverify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverify',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='emailverify',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='emailverify',
            name='otp_creation_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Creation Date'),
        ),
        migrations.AddField(
            model_name='emailverify',
            name='otp_use_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Otp Use time'),
        ),
    ]
