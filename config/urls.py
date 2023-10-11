from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginViewSet.as_view(), name='token_obtain_pair'),
    path('', include('app.urls')),
]