# Generated by Django 3.2.2 on 2022-07-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0029_teamchallenge_kpi_name_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcampaign',
            name='kpi_name_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
