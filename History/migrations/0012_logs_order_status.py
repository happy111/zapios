# Generated by Django 2.1.8 on 2020-09-23 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0047_auto_20200915_1433'),
        ('History', '0011_logs_relevance'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='order_status',
            field=models.ForeignKey(blank=True, limit_choices_to={'active_status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Logs_order_status', to='Orders.OrderStatusType', verbose_name='Order Status'),
        ),
    ]