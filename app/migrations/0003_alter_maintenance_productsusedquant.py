# Generated by Django 4.2.4 on 2023-10-05 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_maintenance_productsusedquant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='productsUsedQuant',
            field=models.IntegerField(null=True),
        ),
    ]
