# Generated by Django 3.2.2 on 2022-07-23 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0018_auto_20220723_1225'),
        ('customer_service_app', '0019_watchtimedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchtimedata',
            name='game_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_user.gamename'),
        ),
    ]
