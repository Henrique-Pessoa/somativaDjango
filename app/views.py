from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter


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
    permission_classes = [
        CustomUserPermission,
    ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"A senha configurada para {user.username} é: {user.password}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username=None):
        if username is not None:
            users = User.objects.filter(username__icontains=username)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        username = self.kwargs.get("username")

        if username:
            return User.objects.filter(username=username)

        queryset = Products.objects.all()
        ordering = self.request.query_params.get("ordering")

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class LoginViewSet(APIView):
    def post(self, request):
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "error": "Credenciais inválidas",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


from rest_framework.filters import OrderingFilter


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["name", "quantityStock"]
    ordering_fields = ["name", "quantityStock"]


class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.objects.all()
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")
        workStation = request.data.get("workStation")

        existing_reserves = Reserve.objects.filter(
            date=date, workStation=workStation
        ).count()

        if existing_reserves >= 2:
            return Response(
                {
                    "detail": "Já existem duas reservas para este dia e posto de trabalho."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MainSerializer

    def verify(self, serializer):
        if Maintenance.objects.count() < 3:
            serializer.save()
        else:
            raise serializers.ValidationError(
                "Não há postos de trabalho disponíveis para a nova manutenção."
            )

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Você precisa estar logado para criar uma nova manutenção."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not (user.is_employee or user.is_superuser):
            return Response(
                {"detail": "Você não tem permissão para criar uma nova manutenção."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Maintenance.objects.count() < 3:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {
                    "detail": "Não há postos de trabalho disponíveis para a nova manutenção."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if (
            user == instance.user
            or user.is_employee
            and user in instance.employeeFk.all()
        ):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Você não tem permissão para excluir esta manutenção."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if (
            user == instance.user
            or user.is_employee
            and user in instance.employeeFk.all()
        ):
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Você não tem permissão para modificar esta manutenção."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Maintenance.objects.filter(user=user)

        return Maintenance.objects.none()


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class VehiclesViewSet(viewsets.ModelViewSet):
    serializer_class = VehiclesSerializer
    queryset = Vehicles.objects.all()
    permission_classes = [IsAuthenticated]


class CategoryServicesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryServicesSerializer
    queryset = CategoryServices.objects.all()
    permission_classes = [CustomAdminPermission]


class ServicesViewSet(viewsets.ModelViewSet):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = [CustomAdminPermission]


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    queryset = Availability.objects.all()
    permission_classes = [CustomAdminPermission]
