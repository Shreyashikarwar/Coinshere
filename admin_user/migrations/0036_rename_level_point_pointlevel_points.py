# Generated by Django 3.2.2 on 2022-08-10 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0035_auto_20220810_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointlevel',
            old_name='level_point',
            new_name='points',
        ),
    ]
