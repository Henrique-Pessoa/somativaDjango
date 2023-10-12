from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"produtos", ProductViewSet, basename="produto")
router.register(r"dias", AvailabilityViewSet, basename="reservaDias")
router.register(r"reservas", ReserveViewSet, basename="reserva")
router.register(r"manutencao", MaintenanceViewSet, basename="pagamento")
router.register(r"pagamento",PaymentsViewSet,basename="pagamento")
router.register(r"veiculos",VehiclesViewSet,basename="veiculos")
urlpatterns = router.urls
