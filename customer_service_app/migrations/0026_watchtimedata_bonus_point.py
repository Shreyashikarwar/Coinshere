# Generated by Django 3.2.2 on 2022-08-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0025_watchtimedata_leader_ship_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchtimedata',
            name='bonus_point',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
