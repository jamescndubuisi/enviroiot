from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _  # Django 4.0
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = False

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print("create user")
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password=None):
        user = self.create_user(email=email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, null=True)
    username = None
    created = models.DateField(auto_now=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class SensorDataPoint(models.Model):
    sensor_name = models.CharField(max_length=100, blank=True, null=True)
    sensor_value = models.CharField(max_length=100, blank=True, null=True)
    sensor_unit = models.CharField(max_length=100, blank=True, null=True)
    sensor_location = models.CharField(max_length=100, blank=True, null=True)
    generated_timestamp = models.DateTimeField(max_length=100, blank=True, null=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)

    def __str__(self):
        return self.sensor_name


class AirData(models.Model):
    temperature_value = models.CharField(max_length=10, blank=True, null=True)
    temperature_unit = models.CharField(max_length=10, blank=True, null=True)
    temperature_celsius = models.CharField(max_length=100, blank=True, null=True)
    temperature_fahrenheit = models.DateTimeField(max_length=100, blank=True, null=True)
    pressure_value = models.CharField(max_length=10, blank=True, null=True)
    pressure_unit = models.CharField(max_length=10, blank=True, null=True)
    humidity_value = models.CharField(max_length=10, blank=True, null=True)
    humidity_unit = models.CharField(max_length=10, blank=True, null=True)
    gas_sensor_resistance = models.CharField(max_length=10, blank=True, null=True)
    generated_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)

    def __str__(self):
        return f"Air Data {self.generated_timestamp} {self.temperature_value} {self.temperature_unit} "


class AirQualityData(models.Model):
    air_quality_index = models.CharField(max_length=10, blank=True, null=True)
    air_quality_class = models.CharField(max_length=10, blank=True, null=True)
    carbon_dioxide_value = models.CharField(max_length=10, blank=True)
    breath_equivalent_voc = models.CharField(max_length=10, blank=True)
    air_quality_calibration_status = models.CharField(max_length=10, blank=True)
    generated_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)

    def __str__(self):
        return f"Air Quality Data {self.generated_timestamp} {self.air_quality_index} {self.air_quality_class} "


class LightData(models.Model):
    light_lux = models.CharField(max_length=10, blank=True, null=True)
    light_unit = models.CharField(max_length=10, blank=True, null=True)
    white_level_balance = models.CharField(max_length=100, blank=True, null=True)
    generated_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)

    def __str__(self):
        return f"Light Data {self.generated_timestamp} {self.light_lux} {self.light_unit} "


class SoundData(models.Model):
    sound_decibel_SPL_dBA = models.CharField(max_length=10, blank=True, null=True)
    sound_unit = models.CharField(max_length=10, blank=True, null=True)
    frequency_band_125 = models.CharField(max_length=100, blank=True, null=True)
    frequency_band_250 = models.CharField(max_length=100, blank=True, null=True)
    frequency_band_500 = models.CharField(max_length=100, blank=True, null=True)
    frequency_band_1000 = models.CharField(max_length=100, blank=True, null=True)
    frequency_band_2000 = models.CharField(max_length=100, blank=True, null=True)
    frequency_band_4000 = models.CharField(max_length=100, blank=True, null=True)
    peak_amp_mPa = models.CharField(max_length=100, blank=True, null=True)
    stable = models.CharField(max_length=100, blank=True, null=True)
    generated_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)

    def __str__(self):
        return f"Sound Data {self.generated_timestamp} {self.sound_decibel_SPL_dBA} {self.sound_unit}"


class ParticleData(models.Model):
    particle_concentration = models.CharField(max_length=10, blank=True, null=True)
    particle_concentration_unit = models.CharField(max_length=10, blank=True, null=True)
    particle_duty_cycle_pc = models.CharField(max_length=10, blank=True, null=True)
    particle_valid = models.CharField(max_length=10, blank=True, null=True)
    generated_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    created_timestamp = models.DateTimeField(max_length=100, auto_now_add=True)
    modified_timestamp = models.DateTimeField(max_length=100, auto_now=True)



