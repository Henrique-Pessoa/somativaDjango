from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

status = [
    ("Pendente", "Pendente"),
    ("Cancelado", "Cancelado"),
    ("Aprovado", "Aprovado"),
]

workStation = [("Posto1", "Posto1"), ("Posto2", "Posto2"), ("Posto3", "Posto3")]


class CustomUserManager(BaseUserManager):
    def create_user(self, name, password, **extra_fields):
        if not name:
            raise ValueError('O campo "username" é obrigatório.')
        if not password:
            raise ValueError('O campo "password" é obrigatório.')
        user = self.model(name=name, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuários devem ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuários devem ter is_superuser=True.")
        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    age = models.IntegerField(null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "email", "password", "is_employee"]

    def __str__(self):
        return self.username


class CategoryServices(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=200)
    valueFinal = models.DecimalField(max_digits=5, decimal_places=2)
    categoryServicesFk = models.ManyToManyField(
        CategoryServices, related_name="services"
    )
    employee = models.ManyToManyField(User, related_name="employeeServices")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            super(Services, self).save(*args, **kwargs)
            self.categoryServicesFk.set(self.categoryServicesFk.all())
            self.employee.set(self.employee.all())
        else:
            super(Services, self).save(*args, **kwargs)


class Products(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    quantityStock = models.IntegerField(null=False, blank=False)
    code = models.CharField(max_length=200, null=False, blank=False)
    manufacturerName = models.CharField(max_length=200, null=False, blank=False)
    valuePur = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False
    )

    def __str__(self):
        return self.name


class Vehicles(models.Model):
    model = models.CharField(max_length=200, null=False, blank=False)
    year = models.DateField(null=False, blank=False)
    category = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.model


class Payments(models.Model):
    category = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=200, choices=status, null=False, blank=False)
    desc = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.category


class Availability(models.Model):
    date = models.DateField()


class Maintenance(models.Model):
    vehiclesFk = models.ForeignKey(
        Vehicles,
        on_delete=models.CASCADE,
        related_name="maintenance",
        null=False,
        blank=False,
    )
    desc = models.CharField(max_length=200, null=False, blank=False)
    productsFk = models.ManyToManyField(Products, related_name="maintenanceTools")
    discount = models.DecimalField(
        decimal_places=2, max_digits=5, null=True, default=0.0
    )
    value = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    user = models.ForeignKey(
        User, related_name="maintenanceUser", on_delete=models.CASCADE
    )
    employeeFk = models.ManyToManyField(
        User,
        related_name="maintenanceEmployees",
    )
    payFk = models.ForeignKey(
        Payments,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="maintenancePay",
    )
    servicesFk = models.ForeignKey(
        Services, on_delete=models.CASCADE, null=False, blank=False
    )
    productsUsedQuant = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.desc

    def save(self, *args, **kwargs):
        super(Maintenance, self).save(*args, **kwargs)

        for product in self.productsFk.all():
            product.quantityStock -= self.productsUsedQuant
            product.save()

        if self.discount is not None:
            self.value -= self.discount


class Reserve(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    date = models.DateField()
    workStation = models.IntegerField()

    class Meta:
        unique_together = ("date", "workStation")

    def save(self, *args, **kwargs):
        existing_reserves = Reserve.objects.filter(
            date=self.date, workStation=self.workStation
        ).count()

        if existing_reserves >= 2:
            raise ValueError(
                "Já existem duas reservas para este dia e posto de trabalho."
            )

        super().save(*args, **kwargs)
