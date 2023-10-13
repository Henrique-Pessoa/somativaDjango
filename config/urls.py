from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginViewSet.as_view(), name="token_obtain_pair"),
    path("registro/", UserCreateViewSet.as_view(), name="registro"),
    path("registro/<str:username>/", UserCreateViewSet.as_view(), name="user-list"),
    path("", include("app.urls")),
]
