from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SensorDataPointViewSet, AirDataPointViewSet, AirQualityDataPointViewSet, SoundDataPointViewSet,
                    LightDataPointViewSet, ParticleDataPointViewSet)

router = DefaultRouter()
router.register(r'', C)
router.register(r'air-data', AirDataPointViewSet)
router.register(r'air-quality-data', AirQualityDataPointViewSet)
router.register(r'sound-data', SoundDataPointViewSet)
router.register(r'light-data', LightDataPointViewSet)
router.register(r'particle-data', ParticleDataPointViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
