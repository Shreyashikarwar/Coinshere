# Generated by Django 3.2.2 on 2022-08-03 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0038_auto_20220728_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managerjoshreason',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='managerjoshreason',
            name='reason_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='line_manager_app.managerreasontype'),
        ),
    ]