# Generated by Django 5.0.4 on 2024-05-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocations', '0003_remove_allocationrequest_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='awarded',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='final',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='requested',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='active',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='expire',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='status',
            field=models.CharField(choices=[('PD', 'Pending'), ('AP', 'Approved'), ('DC', 'Declined'), ('CR', 'Changes Requested')], default='PD', max_length=2),
        ),
        migrations.AlterField(
            model_name='allocationrequest',
            name='submitted',
            field=models.DateField(auto_now=True),
        ),
    ]
