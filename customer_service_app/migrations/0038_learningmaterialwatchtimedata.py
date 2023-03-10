# Generated by Django 3.2.2 on 2022-08-04 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_userprofile_device_id'),
        ('admin_user', '0033_auto_20220804_1152'),
        ('customer_service_app', '0037_readskillandhobbydata'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningMaterialWatchTimeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spent_time', models.CharField(max_length=10, null=True)),
                ('learning_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_user.learningmaterial')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
