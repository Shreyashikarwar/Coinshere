# Generated by Django 3.2.2 on 2022-08-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service_app', '0027_auto_20220801_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerplayedgame',
            name='is_end',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
