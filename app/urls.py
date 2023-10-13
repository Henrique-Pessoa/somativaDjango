from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"produtos", ProductViewSet, basename="produto")
router.register(r"reservas", ReserveViewSet, basename="reserva")
router.register(r"manutencao", MaintenanceViewSet, basename="pagamento"),
router.register(r"dias", AvailabilityViewSet, basename="dias")
router.register(r"pagamentos", PaymentsViewSet, basename="pagamento")
router.register(r"veiculos", VehiclesViewSet, basename="veiculos")
router.register(r"servicos", ServicesViewSet, basename="servicos")
router.register(r"categorias", CategoryServicesViewSet, basename="categoria")
urlpatterns = router.urls
