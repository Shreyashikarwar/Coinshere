# Generated by Django 3.2.2 on 2022-08-05 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0042_healthmetric_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthmetric',
            name='active',
            field=models.IntegerField(default=1),
        ),
    ]
