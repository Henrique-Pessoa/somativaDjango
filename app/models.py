from django.db import models

status = [
    ("Pendente", "Pendente"),
    ("Cancelado", "Cancelado"),
    ("Aprovado", "Aprovado"),
]

workStation = [("Posto1", "Posto1"), ("Posto2", "Posto2"), ("Posto3", "Posto3")]


class CustomUserManager(models.Manager):
    def create_user(self, name, password, email, age, **extra_fields):
        if not name:
            raise ValueError('O campo "username" é obrigatório.')
        if not password:
            raise ValueError('O campo "password" é obrigatório.')
        if not email:
            raise ValueError('O campo "email" é obrigatório.')
        if not age:
            raise ValueError('O campo "age" é obrigatório.')

        user = self.model(username=name, email=email, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["name", "age", "email", "password"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["name", "age", "email", "password"]

    def __str__(self):
        return self.name


class CategoryServices(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    value = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    valueFinal = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False
    )
    categoryServicesFk = models.ManyToManyField(
        CategoryServices, related_name="services"
    )
    employee = models.ManyToManyField(Employee, related_name="employeeServices")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        total_value = sum(category.value for category in self.categoryServicesFk.all())
        self.valueFinal = total_value
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


class Reserve(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    workStation = models.CharField(
        max_length=200, choices=workStation, null=False, blank=False
    )
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.name


class Availability(models.Model):
    reserveFk = models.ForeignKey(
        Reserve, related_name="bookingAvailability", on_delete=models.CASCADE, default=1
    )
    date = models.DateField()

    def __str__(self):
        return str(self.reserveFk)


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
    employeeFk = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
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
    availabilityFk = models.ForeignKey(
        Availability, on_delete=models.CASCADE, null=False, blank=False
    )
    productsUsedQuant = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.desc

    def save(self, *args, **kwargs):
        self.quantityStock -= self.productsUsedQuant
        super(Products, self).save(*args, **kwargs)
