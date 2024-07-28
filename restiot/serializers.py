from rest_framework import serializers
from .models import SensorDataPoint


class SensorDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDataPoint
        fields = '__all__'
