# Generated by Django 3.2.2 on 2022-08-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_userprofile_is_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organiztaion',
            name='password',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
