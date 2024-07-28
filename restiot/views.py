# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import SensorDataPoint
from rest_framework import generics
from .serializers import SensorDataPointSerializer


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

