# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import SensorDataPoint, AirData, AirQualityData, SoundData, LightData, ParticleData
from .serializers import SensorDataPointSerializer, AirDataSerializer, AirQualityDataSerializer, SoundDataSerializer, \
    LightDataSerializer, ParticleDataSerializer


# class SensorDataViewSet(viewsets.ModelViewSet):
#     queryset = SensorDataPoint.objects.all()
#     serializer_class = SensorDataPointSerializer
#     permission_classes = [IsAuthenticated]


# class SensorDataPointListCreateView(generics.ListCreateAPIView):
#     queryset = SensorDataPoint.objects.all()
#     serializer_class = SensorDataPointSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#
# class SensorDataPointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = SensorDataPoint.objects.all()
#     serializer_class = SensorDataPointSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#
# class SensorDataPointViewSet(viewsets.ViewSet):
#     queryset = SensorDataPoint.objects.all()
#     serializer_class = SensorDataPointSerializer
#     permission_classes = [IsAuthenticated]
#     def list(self, request):
#         return SensorDataPointListCreateView(request).list(request)
#
#     def create(self, request):
#         return SensorDataPointListCreateView(request).create(request)
#
#     def retrieve(self, request, pk=None):
#         return SensorDataPointRetrieveUpdateDestroyView(request, pk).retrieve(request,pk)
#
#     def update(self, request, pk=None):
#         return SensorDataPointRetrieveUpdateDestroyView(request, pk).update(request,pk)
#
#     def destroy(self, request, pk=None):
#         return SensorDataPointRetrieveUpdateDestroyView(request, pk).destroy(request,pk)


# Assuming SensorDataViewSet is intended to handle all CRUD operations
# class SensorDataViewSet(viewsets.ModelViewSet):
#     queryset = SensorDataPoint.objects.all()
#     serializer_class = SensorDataPointSerializer
#     permission_classes = [IsAuthenticated]
#

# class SensorDataPointViewSet(viewsets.ViewSet):
#     queryset = SensorDataPoint.objects.all()
#
#     def list(self, request):
#         return generics.ListCreateAPIView.as_view()(request)
#
#     def create(self, request):
#         return generics.ListCreateAPIView.as_view()(request)
#
#     def retrieve(self, request, pk=None):
#         return generics.RetrieveUpdateDestroyAPIView.as_view()(request, pk=pk)
#
#     def update(self, request, pk=None):
#         return generics.RetrieveUpdateDestroyAPIView.as_view()(request, pk=pk)
#
#     def destroy(self, request, pk=None):
#         return generics.RetrieveUpdateDestroyAPIView.as_view()(request, pk=pk)
#


class SensorDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = SensorDataPoint.objects.all()
    serializer_class = SensorDataPointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AirDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = AirData.objects.all()
    serializer_class = AirDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AirQualityDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = AirQualityData.objects.all()
    serializer_class = AirQualityDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class LightDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = LightData.objects.all()
    serializer_class = LightDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SoundDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = SoundData.objects.all()
    serializer_class = SoundDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ParticleDataPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sensor data points to be viewed or edited.
    """
    queryset = ParticleData.objects.all()
    serializer_class = ParticleDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CombineSensorListView(ListAPIView):
    serializer_class_particle = ParticleDataSerializer
    serializer_class_light = LightDataSerializer
    serializer_class_sound = SoundDataSerializer
    serializer_class_air_quality = AirQualityDataSerializer
    serializer_class_air = AirDataSerializer
    serializer_class_sensor = SensorDataPointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset_particle(self):
        return ParticleData.objects.all()

    def get_queryset_light(self):
        return LightData.objects.all()

    def get_queryset_sound(self):
        return SoundData.objects.all()

    def get_queryset_air(self):
        return AirData.objects.all()

    def get_queryset_air_quality(self):
        return AirQualityData.objects.all()

    def get_queryset_sensor(self):
        return SensorDataPoint.objects.all()

    def list(self, request, *args, **kwargs):
        particle_data = ParticleDataSerializer(ParticleData.objects.all(), many=True).data
        light_data = LightDataSerializer(LightData.objects.all(), many=True).data
        sound_data = SoundDataSerializer(SoundData.objects.all(), many=True).data
        air_quality_data = AirQualityDataSerializer(AirQualityData.objects.all(), many=True).data
        air_data = AirDataSerializer(AirData.objects.all(), many=True).data
        sensor_data = SensorDataPointSerializer(SensorDataPoint.objects.all(), many=True).data

        combined_data = {
            'particle_data': particle_data,
            'light_data': light_data,
            'sound_data': sound_data,
            'air_quality_data': air_quality_data,
            'air_data': air_data,
            'sensor_data': sensor_data,
        }

        return Response(combined_data)


class CombineListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        particle_data = ParticleDataSerializer(ParticleData.objects.all(), many=True).data
        light_data = LightDataSerializer(LightData.objects.all(), many=True).data
        sound_data = SoundDataSerializer(SoundData.objects.all(), many=True).data
        air_quality_data = AirQualityDataSerializer(AirQualityData.objects.all(), many=True).data
        air_data = AirDataSerializer(AirData.objects.all(), many=True).data
        sensor_data = SensorDataPointSerializer(SensorDataPoint.objects.all(), many=True).data

        combined_data = {
            'particle_data': particle_data,
            'light_data': light_data,
            'sound_data': sound_data,
            'air_quality_data': air_quality_data,
            'air_data': air_data,
            'sensor_data': sensor_data,
        }

        return Response(combined_data)

