# Generated by Django 4.2.4 on 2023-10-05 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='productsUsedQuant',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
