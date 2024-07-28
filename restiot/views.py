# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SensorData
from .serializers import SensorDataSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    permission_classes = [IsAuthenticated]