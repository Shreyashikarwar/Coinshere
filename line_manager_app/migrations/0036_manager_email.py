# Generated by Django 3.2.2 on 2022-07-26 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0035_auto_20220725_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
