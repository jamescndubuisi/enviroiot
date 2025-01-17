"""
URL configuration for cvgpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (login_page, homepage, sign_up, AirDataChartView, AirQualityDataChartView,
                    air_data_json, air_quality_data_json, AirDataPlotlyView, light_data_json,
                    LightDataChartView, ParticleDataChartView, particle_data_json, AirDataBoxView, sound_data_json,
                    SoundDataChartView, AirQualityLightDataChartView)

urlpatterns = [
    path('', homepage, name="home"),
    path('login', login_page, name='signin'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', sign_up, name="register"),
    path('air-data-chart/', AirDataChartView.as_view(), name='air_data_chart'),

    path('airplotlychart/', AirDataPlotlyView.as_view(), name='air_data_plotly_chart'),
    path('air-data-json/', air_data_json, name='air_data_json'),

    path('air-quality-data-chart/', AirQualityDataChartView.as_view(), name='air_quality_data_chart'),
    path('airquality-data-json/', air_quality_data_json, name='airquality_data_json'),

    path('light-data-json/', light_data_json, name='light_data_json'),
    path('light-data-chart/', LightDataChartView.as_view(), name='light_data_chart'),
    path('particle-data-json/', particle_data_json, name='particle_data_json'),
    path('particle-data-chart/', ParticleDataChartView.as_view(), name='particle_data_chart'),
    path('air-data-boxes/', AirDataBoxView.as_view(), name='air_data_boxes'),
    path('sound-data-json/', sound_data_json, name='sound_data_json'),
    path('sound-data-charts/', SoundDataChartView.as_view(), name='sound_data_chart'),
    path('air-quality-sound-data-charts/', AirQualityLightDataChartView.as_view(), name='air_quality_light_data_chart'),

]
