# Generated by Django 3.2.2 on 2022-07-26 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0019_rename_organizationperformancedata_organizationemployeeperformancedata'),
        ('customer_service_app', '0024_auto_20220725_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchtimedata',
            name='leader_ship_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_user.leadershiptask'),
        ),
    ]
