# Generated by Django 3.2.2 on 2022-08-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0027_avatarimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadershiptask',
            name='is_seen',
            field=models.IntegerField(default=0),
        ),
    ]