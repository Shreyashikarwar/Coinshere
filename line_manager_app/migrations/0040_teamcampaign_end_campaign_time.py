# Generated by Django 3.2.2 on 2022-08-04 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0039_auto_20220803_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcampaign',
            name='end_campaign_time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
