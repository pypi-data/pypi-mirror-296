# Generated by Django 3.2.23 on 2024-09-09 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sap_success_factors', '0023_auto_20240909_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='key',
        ),
        migrations.RemoveField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='secret',
        ),
    ]
