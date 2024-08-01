from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import SensorDataPoint, AirData, AirQualityData, SoundData, LightData, ParticleData
from django.shortcuts import HttpResponse
from rest_framework.response import Response


class SensorDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDataPoint
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp']


class AirDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirData
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp']


class AirQualityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityData
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp',
                   "air_quality_calibration_meaning", "air_quality_class"]


class SoundDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoundData
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp', 'sound_unit']


class LightDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightData
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp', "light_unit"]


class ParticleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticleData
        exclude = ['generated_timestamp', 'created_timestamp', 'modified_timestamp', 'particle_concentration_unit']


class CombinedDataSerializer(serializers.Serializer):
    sensor_data_point = serializers.SerializerMethodField()
    air_data = serializers.SerializerMethodField()
    air_quality_data = serializers.SerializerMethodField()
    light_data = serializers.SerializerMethodField()
    sound_data = serializers.SerializerMethodField()
    particle_data = serializers.SerializerMethodField()

    def get_sensor_data_point(self):
        # Example: Fetch and return the latest SensorDataPoint
        sensor_data_point = SensorDataPoint.objects.latest('id')
        serializer = SensorDataPointSerializer(sensor_data_point)
        return serializer.data

    def get_air_data(self):
        air_data = AirData.objects.latest('id')
        serializer = AirDataSerializer(air_data)
        return serializer.data

    def get_airquality_data(self):
        air_data = AirQualityData.objects.latest('id')
        serializer = AirQualityDataSerializer(air_data)
        return serializer.data

    def get_particle_data(self):
        air_data = ParticleData.objects.latest('id')
        serializer = ParticleDataSerializer(air_data)
        return serializer.data

    def get_light_data(self):
        air_data = LightData.objects.latest('id')
        serializer = LightDataSerializer(air_data)
        return serializer.data

    def get_sound_data(self):
        air_data = SoundData.objects.latest('id')
        serializer = SoundDataSerializer(air_data)
        return serializer.data

    # Repeat similar methods for air_quality_data, light_data, sound_data, particle_data


