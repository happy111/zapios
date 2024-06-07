# Generated by Django 2.1.8 on 2020-10-17 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Outlet', '0055_auto_20201017_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletprofile',
            name='auth_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instaoutlet_profile_auth_user', to=settings.AUTH_USER_MODEL),
        ),
    ]