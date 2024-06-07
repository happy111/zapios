# Generated by Django 2.1.8 on 2020-07-23 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRole', '0027_billrollpermission_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerprofile',
            name='login_type',
            field=models.CharField(choices=[('android', 'Android'), ('ios', 'IOS'), ('web', 'Web')], default=1, max_length=255, verbose_name='Login Type'),
            preserve_default=False,
        ),
    ]