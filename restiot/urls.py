from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CombineListView,CombineSensorListView, AirDataPointViewSet, AirQualityDataPointViewSet,
                    SoundDataPointViewSet,
                    LightDataPointViewSet, ParticleDataPointViewSet)

router = DefaultRouter()
router.register(r'air-data', AirDataPointViewSet)
router.register(r'air-quality-data', AirQualityDataPointViewSet)
router.register(r'sound-data', SoundDataPointViewSet)
router.register(r'light-data', LightDataPointViewSet)
router.register(r'particle-data', ParticleDataPointViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('combined/', CombineListView.as_view()),
    path('combined/', CombineSensorListView.as_view() ),
]
