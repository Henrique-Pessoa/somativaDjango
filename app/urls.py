from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"registrar", CreateUserViewSet, basename="registrar")
router.register(r"produtos", ProductViewSet, basename="produto")
router.register(r"dias", AvailabilityViewSet, basename="reserva")
router.register(r"reservas", ReserveViewSet, basename="reserva")
router.register(r"manutencao", MaintenanceViewSet, basename="maintenance")

urlpatterns = router.urls
