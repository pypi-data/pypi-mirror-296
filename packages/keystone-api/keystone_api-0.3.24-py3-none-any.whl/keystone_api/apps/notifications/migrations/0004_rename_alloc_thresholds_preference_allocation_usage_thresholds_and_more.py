# Generated by Django 5.0.8 on 2024-08-29 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preference',
            old_name='alloc_thresholds',
            new_name='allocation_usage_thresholds',
        ),
        migrations.RenameField(
            model_name='preference',
            old_name='expiry_thresholds',
            new_name='request_expiry_thresholds',
        ),
    ]
