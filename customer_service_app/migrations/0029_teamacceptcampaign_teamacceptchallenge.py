# Generated by Django 3.2.2 on 2022-08-02 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0038_auto_20220728_1507'),
        ('customer_service_app', '0028_alter_customerplayedgame_is_end'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamAcceptChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_accepted_id', models.IntegerField(blank=True, null=True)),
                ('is_accepted', models.IntegerField(default=0)),
                ('team_challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.teamchallenge')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamAcceptCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_accepted_id', models.IntegerField(blank=True, null=True)),
                ('is_accepted', models.IntegerField(default=0)),
                ('team_campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.teamcampaign')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
