# Generated by Django 3.2.2 on 2022-08-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0028_leadershiptask_is_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=220, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
