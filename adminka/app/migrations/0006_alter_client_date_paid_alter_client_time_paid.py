# Generated by Django 5.1.3 on 2025-05-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_client_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_paid',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='time_paid',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
