# Generated by Django 3.2.2 on 2022-07-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0005_auto_20220718_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadershiptask',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]