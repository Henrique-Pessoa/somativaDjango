# Generated by Django 4.2.4 on 2023-10-13 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('age', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Cancelado', 'Cancelado'), ('Aprovado', 'Aprovado')], max_length=200)),
                ('desc', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('quantityStock', models.IntegerField()),
                ('code', models.CharField(max_length=200)),
                ('manufacturerName', models.CharField(max_length=200)),
                ('valuePur', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=200)),
                ('year', models.DateField()),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('valueFinal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('categoryServicesFk', models.ManyToManyField(related_name='services', to='app.categoryservices')),
                ('employee', models.ManyToManyField(related_name='employeeServices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=200)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('productsUsedQuant', models.IntegerField(null=True)),
                ('employeeFk', models.ManyToManyField(related_name='maintenanceEmployees', to=settings.AUTH_USER_MODEL)),
                ('payFk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenancePay', to='app.payments')),
                ('productsFk', models.ManyToManyField(related_name='maintenanceTools', to='app.products')),
                ('servicesFk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.services')),
                ('user', models.ManyToManyField(related_name='maintenanceUser', to=settings.AUTH_USER_MODEL)),
                ('vehiclesFk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance', to='app.vehicles')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('work_station', models.IntegerField()),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.maintenance')),
            ],
            options={
                'unique_together': {('date', 'work_station')},
            },
        ),
    ]
