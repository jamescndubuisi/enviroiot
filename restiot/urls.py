from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorDataPointViewSet

router = DefaultRouter()
router.register(r'', SensorDataPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]