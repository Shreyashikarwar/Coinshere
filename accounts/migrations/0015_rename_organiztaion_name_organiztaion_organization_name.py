# Generated by Django 3.2.13 on 2022-07-01 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20220701_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organiztaion',
            old_name='organiztaion_name',
            new_name='organization_name',
        ),
    ]
