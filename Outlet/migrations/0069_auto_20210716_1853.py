# Generated by Django 2.1.8 on 2021-07-16 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Outlet', '0068_auto_20210716_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outletprofile',
            name='aggre_store_action_ref_id',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='is_synced',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='last_synced_at',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='swiggy_open_status',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='sync_request_id',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='sync_status',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='urban_event',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='urbanpiper_store_id',
        ),
        migrations.RemoveField(
            model_name='outletprofile',
            name='zomato_open_status',
        ),
    ]
