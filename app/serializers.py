from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        field = '__all__'
        
class CategoryServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryServices
        field = '__all__'
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        field = '__all__'
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        field = '__all__'
class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        field = '__all__'
        
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        field = '__all__'
class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        field = '__all__'
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        field = '__all__'
class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        field = '__all__'
        