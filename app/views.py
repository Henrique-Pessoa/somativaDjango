from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


class CustomUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class CustomAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class UserCreateViewSet(APIView):
    permission_classes=[CustomUserPermission,]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"A senha configurada para {user.username} é: {user.password}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        User = get_user_model()  
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LoginViewSet(APIView):
    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        quantityStock = self.request.query_params.get("quantityStock")
        if quantityStock is not None:
            self.queryset = self.queryset.filter(quantityStock=int(quantityStock))
        return self.queryset


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    queryset = Availability.objects.all()
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")
        existingAvailability = Availability.objects.filter(date=date)

        if existingAvailability.exists():
            return Response(
                "Esta data já está reservada.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.all()
    permission_classes = [IsAdminUser]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MainSerializer

    def perform_create(self, serializer):
        if Maintenance.objects.count() < 2:
            serializer.save()
        else:
            "Não há postos de trabalho disponíveis para a nova manutenção."


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.all()
    permission_classes = [IsAuthenticated]


class VehiclesViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.all()
    permission_classes = [IsAuthenticated]
