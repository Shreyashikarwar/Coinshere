# Generated by Django 3.2.13 on 2022-06-30 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_firebase_token'),
        ('line_manager_app', '0007_alter_teamcampaign_criteria_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerConcernType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManagerRaiseConcern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100)),
                ('action_owner_id', models.IntegerField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(default=1)),
                ('concern_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.managerconcerntype')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
