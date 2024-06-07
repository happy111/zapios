# Generated by Django 2.1.8 on 2021-03-02 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('email', models.CharField(max_length=20, verbose_name='Email')),
                ('otp', models.CharField(blank=True, max_length=20, null=True, verbose_name='Email OTP')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date')),
            ],
            options={
                'verbose_name': '    Email Verify',
                'verbose_name_plural': '    Email Verify',
            },
        ),
    ]