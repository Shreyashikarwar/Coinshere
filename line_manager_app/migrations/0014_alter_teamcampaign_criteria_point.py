# Generated by Django 3.2.13 on 2022-07-01 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0013_auto_20220701_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamcampaign',
            name='criteria_point',
            field=models.ManyToManyField(to='line_manager_app.CriteriaPoint'),
        ),
    ]
