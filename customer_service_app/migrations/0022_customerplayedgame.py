# Generated by Django 3.2.2 on 2022-07-23 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_userprofile_is_signup'),
        ('admin_user', '0018_auto_20220723_1225'),
        ('customer_service_app', '0021_remove_watchtimedata_game_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPlayedGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spent_time', models.CharField(max_length=10, null=True)),
                ('game_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_user.gamename')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]