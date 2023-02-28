# Generated by Django 3.2.13 on 2022-06-30 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengePurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('purpose_name', models.CharField(max_length=100)),
                ('status', models.ImageField(default=1, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]