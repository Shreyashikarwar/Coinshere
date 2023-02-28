# Generated by Django 3.2.2 on 2022-07-22 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0030_teamcampaign_kpi_name_id'),
        ('admin_user', '0013_organizationemployeedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationemployeedata',
            name='designation',
            field=models.CharField(max_length=320, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='email',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='emp_code',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='gender',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='language',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='location',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='line_manager_app.manager'),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='mobile_no',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organizationemployeedata',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='line_manager_app.team'),
        ),
    ]