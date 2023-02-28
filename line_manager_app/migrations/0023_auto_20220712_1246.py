# Generated by Django 3.2.2 on 2022-07-12 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20220712_1242'),
        ('line_manager_app', '0022_auto_20220712_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team_name', models.CharField(max_length=100)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.organiztaion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='managerteamprofile',
            name='manager_org',
        ),
        migrations.DeleteModel(
            name='ManagerorOrganization',
        ),
        migrations.DeleteModel(
            name='ManagerTeamProfile',
        ),
        migrations.AddField(
            model_name='manager',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.team'),
        ),
    ]
