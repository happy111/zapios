# Generated by Django 2.1.8 on 2021-06-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0008_auto_20210420_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
                ('content', models.CharField(blank=True, max_length=200, null=True, verbose_name='Content')),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('complete', 'Complete')], max_length=50, null=True, verbose_name='Status')),
                ('active_status', models.BooleanField(default=0, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': '    Notice Card',
                'verbose_name_plural': '    Notice Card',
            },
        ),
    ]
