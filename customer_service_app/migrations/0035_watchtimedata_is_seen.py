# Generated by Django 3.2.2 on 2022-08-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0034_auto_20220803_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchtimedata',
            name='is_seen',
            field=models.IntegerField(default=0),
        ),
    ]
