# Generated by Django 3.2.13 on 2022-06-30 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_firebase_token'),
        ('line_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('challenge_name', models.CharField(max_length=50)),
                ('start_time', models.CharField(max_length=20)),
                ('end_time', models.CharField(max_length=20)),
                ('activity_details', models.CharField(max_length=200)),
                ('bonus_point', models.IntegerField()),
                ('challenge_purpose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.challengepurpose')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
