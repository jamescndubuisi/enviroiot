from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from restiot.models import AirData, AirQualityData, LightData, ParticleData, SoundData, SensorDataPoint, User
from . import forms
from django.http import JsonResponse

# Create your views here.


@login_required
def homepage(request):
    title = "Enviroiot"
    return render(request, "webiot/index.html", {"title": title})


def login_page(request):
    title = "Login"
    message = ""
    purpose = "Login"
    form = forms.LoginForm
    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user=user)
                return redirect("home")
            else:
                messages.error(request, 'username or password not correct')
                return redirect('log_in')
        else:
            print("Terrible form")
            return render(
                request, "registration/login.html", {"form": form, "message": message}
            )
    return render(
        request,
        "registration/login.html",
        {"form": form, "message": message, "title": title, "purpose": purpose},
    )


def sign_up(request):
    title = "Register"
    context = {"title": title}
    form = forms.CreateUser(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'registration/register.html')
    context['form'] = form
    return render(request, 'registration/register.html', context)


def create_charts(requests):
    return render(requests, 'webiot/charts.html', {})


class AirDataChartView(TemplateView):
    template_name = 'webiot/airdatachart.html'


class AirQualityDataChartView(TemplateView):
    template_name = 'webiot/airqualitydata.html'


class AirDataPlotlyView(TemplateView):
    template_name = 'webiot/plotlycharts.html'


class AirDataBoxView(TemplateView):
    template_name = 'webiot/airdataboxes.html'

def air_data_json(request):
    data = AirData.objects.order_by('-generated_timestamp')[:100]  # Last 100 entries
    return JsonResponse({
        'labels': [entry.generated_timestamp.strftime('%Y-%m-%d %H:%M:%S') for entry in data],
        'temperature': [entry.temperature_celsius for entry in data],
        'humidity': [entry.humidity_value for entry in data],
        'pressure': [entry.pressure_value for entry in data],
    })


def air_quality_data_json(request):
    data = AirQualityData.objects.order_by('-generated_timestamp')[:100]  # Last 100 entries
    return JsonResponse({
        'labels': [entry.generated_timestamp.strftime('%Y-%m-%d %H:%M:%S') for entry in data],
        'airqualityindex': [entry.air_quality_index for entry in data],
        'carbondioxide': [entry.carbon_dioxide_value for entry in data],
        'breathequivalentvoc': [entry.breath_equivalent_voc for entry in data],
    })


def light_data_json(request):
    data = LightData.objects.order_by('-generated_timestamp')[:100]  # Last 100 entries
    return JsonResponse({
        'labels': [entry.generated_timestamp.strftime('%Y-%m-%d %H:%M:%S') for entry in data],
        'light_lux': [entry.light_lux for entry in data],
        'white_level_balance': [entry.white_level_balance for entry in data],
    })

class LightDataChartView(TemplateView):
    template_name = 'webiot/lightdatachart.html'


def particle_data_json(request):
    data = ParticleData.objects.order_by('-generated_timestamp')[:100]  # Last 100 entries
    return JsonResponse({
        'labels': [entry.generated_timestamp.strftime('%Y-%m-%d %H:%M:%S') for entry in data],
        'particle_concentration': [entry.particle_concentration for entry in data],
        'particle_duty_cycle_pc': [entry.particle_duty_cycle_pc for entry in data],
        'particle_valid': [entry.particle_valid for entry in data],
    })


class ParticleDataChartView(TemplateView):
    template_name = 'webiot/particledatachart.html'


# class HomeDataChartView(TemplateView):
#     template_name = 'webiot/index.html'
