# Generated by Django 3.2.2 on 2022-08-18 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_organiztaion_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_updated',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
