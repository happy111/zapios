# Generated by Django 2.1.8 on 2021-06-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0047_managerprofile_is_firstuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerprofile',
            name='is_hide',
            field=models.BooleanField(default=0, verbose_name='Is Hide'),
        ),
    ]