# Generated by Django 5.0.4 on 2024-04-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_ldap_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchgroup',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
