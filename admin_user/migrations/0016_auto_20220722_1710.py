# Generated by Django 3.2.2 on 2022-07-22 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line_manager_app', '0030_teamcampaign_kpi_name_id'),
        ('admin_user', '0015_organizationperformancedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_actuals',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_name_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='line_manager_app.kpiname'),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_status',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_target',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='kpi_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='organization_employee_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_user.organizationemployeedata'),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='permormance_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organizationperformancedata',
            name='target_time_period',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
