# Generated by Django 3.2.2 on 2022-07-18 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0003_winlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherlink',
            name='image_data',
            field=models.ImageField(default=0, upload_to='OtherLink/image/'),
        ),
        migrations.AddField(
            model_name='otherlink',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
