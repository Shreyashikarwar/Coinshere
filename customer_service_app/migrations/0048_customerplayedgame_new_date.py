# Generated by Django 3.2.2 on 2022-08-23 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0047_watchtimedata_bonus_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerplayedgame',
            name='new_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
