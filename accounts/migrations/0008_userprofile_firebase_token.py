# Generated by Django 3.2.13 on 2022-06-29 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_userprofile_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='firebase_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
