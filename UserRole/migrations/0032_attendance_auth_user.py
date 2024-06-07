# Generated by Django 2.1.8 on 2020-10-24 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserRole', '0031_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='auth_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Attendance_auth_user', to=settings.AUTH_USER_MODEL),
        ),
    ]