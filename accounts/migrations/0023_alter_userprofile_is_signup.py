# Generated by Django 3.2.2 on 2022-07-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_userprofile_is_signup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_signup',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
