# Generated by Django 4.2.4 on 2023-10-13 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='user',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='maintenanceUser', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]