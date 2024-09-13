# Generated by Django 4.2.7 on 2024-02-26 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('allocations', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationrequestreview',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allocationrequest',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.researchgroup'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allocations.cluster'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allocations.allocationrequest'),
        ),
    ]
