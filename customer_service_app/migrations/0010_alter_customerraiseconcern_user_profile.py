# Generated by Django 3.2.2 on 2022-07-06 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_userprofile_role'),
        ('customer_service_app', '0009_alter_customerraiseconcern_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerraiseconcern',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile'),
            preserve_default=False,
        ),
    ]