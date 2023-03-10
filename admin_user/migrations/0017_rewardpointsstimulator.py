# Generated by Django 3.2.2 on 2022-07-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0016_auto_20220722_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardPointsStimulator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.CharField(max_length=120, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('points', models.CharField(max_length=120, null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('multiplier', models.FloatField(max_length=120, null=True)),
                ('units', models.FloatField(null=True)),
                ('no_of_days', models.IntegerField(null=True)),
                ('score', models.FloatField(null=True)),
                ('inr', models.FloatField(null=True)),
                ('percent', models.CharField(max_length=120, null=True)),
                ('status', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
