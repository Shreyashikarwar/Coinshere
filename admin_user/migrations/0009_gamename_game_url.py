# Generated by Django 3.2.2 on 2022-07-19 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0008_gamename'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamename',
            name='game_url',
            field=models.URLField(null=True),
        ),
    ]
