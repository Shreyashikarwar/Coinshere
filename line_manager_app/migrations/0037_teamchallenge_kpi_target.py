# Generated by Django 3.2.2 on 2022-07-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0036_manager_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamchallenge',
            name='kpi_target',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
