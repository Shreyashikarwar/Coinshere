# Generated by Django 3.2.13 on 2022-06-30 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0003_customerconcerntype_customerraiseconcern'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerConcernType',
            new_name='CustomerConcernCategory',
        ),
    ]
