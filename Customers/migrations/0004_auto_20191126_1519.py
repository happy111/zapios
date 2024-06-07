# Generated by Django 2.1.8 on 2019-11-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0003_auto_20191124_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerprofile',
            old_name='Company',
            new_name='company',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='mobile_with_isd',
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Mobile No'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='active_status',
            field=models.BooleanField(default=0, verbose_name='Is Active'),
        ),
    ]
