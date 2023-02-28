# Generated by Django 3.2.2 on 2022-08-22 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_alter_organiztaion_password'),
        ('admin_user', '0043_delete_organizationtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='accounts.organiztaion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
