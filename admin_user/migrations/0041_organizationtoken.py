# Generated by Django 3.2.2 on 2022-08-22 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_userprofile_is_updated'),
        ('admin_user', '0040_remove_avatarimage_is_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to='accounts.organiztaion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
