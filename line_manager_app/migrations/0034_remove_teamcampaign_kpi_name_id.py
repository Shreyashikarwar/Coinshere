# Generated by Django 3.2.2 on 2022-07-23 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0033_criteriapoint_kpi_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamcampaign',
            name='kpi_name_id',
        ),
    ]