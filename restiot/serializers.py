from rest_framework import serializers
from .models import SensorDataPoint,AirData, AirQualityData, SoundData, LightData, ParticleData


class SensorDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDataPoint
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']


class AirDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirData
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']


class AirQualityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityData
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']


class SoundDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundData
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']


class LightDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightData
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']


class ParticleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticleData
        exclude = ['generated_timestamp','created_timestamp','modified_timestamp']

