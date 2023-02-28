# Generated by Django 3.2.2 on 2022-07-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0023_auto_20220712_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndustryWorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=90, null=True)),
                ('status', models.IntegerField(default=1, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]