# Generated by Django 3.2.13 on 2022-06-30 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_firebase_token'),
        ('customer_service_app', '0005_rename_concern_type_customerraiseconcern_concern_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyReward',
            new_name='MyRewardPoint',
        ),
    ]