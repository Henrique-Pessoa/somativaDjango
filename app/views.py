from django.shortcuts import render
from rest_framework import viewsets,status
from serializers import *
from models import *
from rest_framework.permissions import BasePermission


class CustomUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated
    

class CreateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CustomUserPermission,)


