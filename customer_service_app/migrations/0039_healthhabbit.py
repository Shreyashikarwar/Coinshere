# Generated by Django 3.2.2 on 2022-08-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0038_learningmaterialwatchtimedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthHabbit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('day', models.IntegerField()),
                ('habbit_of_the_day', models.CharField(max_length=100)),
                ('theme', models.CharField(max_length=20)),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
