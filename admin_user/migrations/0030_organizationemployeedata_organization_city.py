# Generated by Django 3.2.2 on 2022-08-03 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0029_organizationcity'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationemployeedata',
            name='organization_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_user.organizationcity'),
        ),
    ]
