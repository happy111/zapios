# Generated by Django 2.1.8 on 2020-11-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffattendance',
            name='active_status',
            field=models.BooleanField(default=0, verbose_name='Login/Logout'),
        ),
    ]