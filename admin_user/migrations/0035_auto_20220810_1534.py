# Generated by Django 3.2.2 on 2022-08-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0034_activitylog'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level_point', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='WinLevel',
        ),
    ]