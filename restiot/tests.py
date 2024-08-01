from datetime import datetime as timezone, timedelta as timedelta
import pytest
from .models import UserManager, User, AirData, AirQualityData, LightData, SoundData, ParticleData


class TestUserManager:

    # Creating a regular user with valid email and password
    def test_create_user_with_valid_email_and_password(self):
        manager = UserManager()
        user = manager.create_user(email="user@example.com", password="password123")
        assert user.email == "user@example.com"
        assert user.check_password("password123")
        assert not user.is_staff
        assert not user.is_superuser

    # Creating a staff user with valid email and password
    def test_create_staff_user_with_valid_email_and_password(self):
        manager = UserManager()
        user = manager.create_staff_user(email="staff@example.com", password="password123")
        assert user.email == "staff@example.com"
        assert user.check_password("password123")
        assert user.is_staff
        assert not user.is_superuser

    # Creating a superuser with valid email and password
    def test_create_superuser_with_valid_email_and_password(self):
        manager = UserManager()
        user = manager.create_superuser(email="superuser@example.com", password="password123")
        assert user.email == "superuser@example.com"
        assert user.check_password("password123")
        assert user.is_staff
        assert user.is_superuser

    # Normalizing email addresses during user creation
    def test_normalize_email_during_user_creation(self):
        manager = UserManager()
        user = manager.create_user(email="USER@EXAMPLE.COM", password="password123")
        assert user.email == "user@example.com"

    # Setting default values for is_superuser and is_staff fields
    def test_default_values_for_is_superuser_and_is_staff(self):
        manager = UserManager()
        user = manager.create_user(email="user@example.com", password="password123")
        assert not user.is_staff
        assert not user.is_superuser

    # Attempting to create a user without an email
    def test_create_user_without_email(self):
        manager = UserManager()
        with pytest.raises(ValueError, match="The given email must be set"):
            manager.create_user(email=None, password="password123")

    # Attempting to create a superuser with is_staff set to False
    def test_create_superuser_with_is_staff_false(self):
        manager = UserManager()
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            manager.create_superuser(email="superuser@example.com", password="password123", is_staff=False)

    # Attempting to create a superuser with is_superuser set to False
    def test_create_superuser_with_is_superuser_false(self):
        manager = UserManager()
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            manager.create_superuser(email="superuser@example.com", password="password123", is_superuser=False)

    # Creating a user with additional fields in extra_fields
    def test_create_user_with_additional_fields(self):
        manager = UserManager()
        user = manager.create_user(email="user@example.com", password="password123", first_name="John", last_name="Doe")
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    # Handling of duplicate email addresses
    def test_handle_duplicate_email_addresses(self):
        manager = UserManager()
        manager.create_user(email="duplicate@example.com", password="password123")
        with pytest.raises(Exception):  # Replace Exception with the specific exception your ORM raises for duplicates
            manager.create_user(email="duplicate@example.com", password="password123")

    # Verifying password hashing during user creation
    def test_verify_password_hashing_during_creation(self):
        manager = UserManager()
        user = manager.create_user(email="user@example.com", password="password123")
        assert not user.password == "password123"
        assert user.check_password("password123")


class TestUser:

    # Creating a user with a valid email and password
    def test_create_user_with_valid_email_and_password(self, db):
        user = User.objects.create_user(email="test@example.com", password="password123")
        assert user.email == "test@example.com"
        assert user.check_password("password123")

    # Retrieving the full name of a user
    def test_get_full_name(self, db):
        user = User.objects.create_user(email="test@example.com", password="password123", first_name="John",
                                        last_name="Doe")
        assert user.get_full_name() == "John Doe"

    # Retrieving the short name of a user
    def test_get_short_name(self, db):
        user = User.objects.create_user(email="test@example.com", password="password123", first_name="John")
        assert user.get_short_name() == "John"

    # Sending an email to a user
    def test_email_user(self, mocker, db):
        mock_send_mail = mocker.patch("restiot.models.send_mail")
        user = User.objects.create_user(email="test@example.com", password="password123")
        user.email_user("Subject", "Message", "from@example.com")
        mock_send_mail.assert_called_once_with("Subject", "Message", "from@example.com", ["test@example.com"])

    # Creating a superuser with the correct attributes
    def test_create_superuser_with_correct_attributes(self, db):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123")
        assert superuser.is_superuser
        assert superuser.is_staff

    # Creating a staff user with the correct attributes
    def test_create_staff_user_with_correct_attributes(self, db):
        staff_user = User.objects.create_staff_user(email="staff@example.com", password="staff123")
        assert staff_user.is_staff
        assert not staff_user.is_superuser

    # Creating a user without an email
    def test_create_user_without_email(self, db):
        with pytest.raises(ValueError, match="The given email must be set"):
            User.objects.create_user(email=None, password="password123")

    # Creating a superuser without setting is_staff to True
    def test_create_superuser_without_is_staff_true(self, db):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_staff=False)

    # Creating a superuser without setting is_superuser to True
    def test_create_superuser_without_is_superuser_true(self, db):
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_superuser=False)

    # Creating a user with an already existing email
    def test_create_user_with_existing_email(self, db):
        User.objects.create_user(email="test@example.com", password="password123")
        with pytest.raises(Exception):
            User.objects.create_user(email="test@example.com", password="password456")

    # Sending an email with missing subject or message
    def test_email_user_with_missing_subject_or_message(self, mocker, db):
        mock_send_mail = mocker.patch("restiot.models.send_mail")
        user = User.objects.create_user(email="test@example.com", password="password123")
        with pytest.raises(TypeError):
            user.email_user(None, "Message", "from@example.com")
        with pytest.raises(TypeError):
            user.email_user("Subject", None, "from@example.com")

    # Ensuring the email field is unique
    def test_email_field_is_unique(self, db):
        User.objects.create_user(email="unique@example.com", password="password123")
        with pytest.raises(Exception):
            User.objects.create_user(email="unique@example.com", password="password456")


class TestAirData:

    # Creating an AirData instance with all fields populated
    def test_create_airdata_all_fields(self):
        airdata = AirData.objects.create(
            temperature_value=25.0,
            temperature_unit='Celsius',
            temperature_celsius=25.0,
            temperature_fahrenheit='2023-01-01T00:00:00Z',
            pressure_value=1013.25,
            pressure_unit='hPa',
            humidity_value=40.0,
            humidity_unit='%',
            gas_sensor_resistance=200.0
        )
        assert airdata.id is not None

    # Creating an AirData instance with only required fields populated
    def test_create_airdata_required_fields(self):
        airdata = AirData.objects.create()
        assert airdata.id is not None

    # Retrieving an AirData instance and verifying field values
    def test_retrieve_airdata(self):
        airdata = AirData.objects.create(temperature_value=25.0)
        retrieved = AirData.objects.get(id=airdata.id)
        assert retrieved.temperature_value == 25.0

    # Updating an AirData instance and verifying modified_timestamp
    def test_update_airdata_modified_timestamp(self):
        airdata = AirData.objects.create(temperature_value=25.0)
        old_timestamp = airdata.modified_timestamp
        airdata.temperature_value = 30.0
        airdata.save()
        assert airdata.modified_timestamp > old_timestamp

    # Deleting an AirData instance and ensuring it is removed from the database
    def test_delete_airdata(self):
        airdata = AirData.objects.create(temperature_value=25.0)
        airdata_id = airdata.id
        airdata.delete()
        with pytest.raises(AirData.DoesNotExist):
            AirData.objects.get(id=airdata_id)

    # Creating an AirData instance with null values for all optional fields
    def test_create_airdata_null_optional_fields(self):
        airdata = AirData.objects.create(
            temperature_value=None,
            temperature_unit=None,
            temperature_celsius=None,
            temperature_fahrenheit=None,
            pressure_value=None,
            pressure_unit=None,
            humidity_value=None,
            humidity_unit=None,
            gas_sensor_resistance=None
        )
        assert airdata.id is not None

    # Creating an AirData instance with maximum length strings for CharField fields
    def test_create_airdata_max_length_strings(self):
        airdata = AirData.objects.create(
            temperature_unit='C' * 10,
            pressure_unit='h' * 10,
            humidity_unit='%' * 10
        )
        assert airdata.id is not None

    # Creating an AirData instance with invalid data types for fields
    def test_create_airdata_invalid_data_types(self):
        with pytest.raises(ValueError):
            AirData.objects.create(temperature_value='invalid')

    # Creating an AirData instance with negative values for FloatField fields
    def test_create_airdata_negative_values(self):
        airdata = AirData.objects.create(temperature_value=-10.0)
        assert airdata.temperature_value == -10.0

    # Creating an AirData instance with future dates for DateTimeField fields
    def test_create_airdata_future_dates(self):
        future_date = '2099-12-31T23:59:59Z'
        airdata = AirData.objects.create(temperature_fahrenheit=future_date)
        assert str(airdata.temperature_fahrenheit) == future_date

    # Verifying the string representation of an AirData instance
    def test_str_representation_airdata(self):
        airdata = AirData.objects.create(
            temperature_value=25.0,
            temperature_unit='Celsius',
            generated_timestamp='2023-01-01T00:00:00Z'
        )
        expected_str = "Air Data 2023-01-01 00:00:00+00:00 25.0 Celsius "
        assert str(airdata) == expected_str

    # Ensuring auto_now_add fields are set only on creation
    def test_auto_now_add_fields_on_creation(self):
        airdata = AirData.objects.create()
        created_timestamp = airdata.created_timestamp
        generated_timestamp = airdata.generated_timestamp

        airdata.save()

        assert airdata.created_timestamp == created_timestamp
        assert airdata.generated_timestamp == generated_timestamp


class TestAirQualityData:

    # Creating an AirQualityData instance with valid data
    def test_create_air_quality_data_with_valid_data(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        assert data.pk is not None

    # Retrieving an AirQualityData instance from the database
    def test_retrieve_air_quality_data(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        retrieved_data = AirQualityData.objects.get(pk=data.pk)
        assert retrieved_data == data

    # Updating an AirQualityData instance with new values
    def test_update_air_quality_data(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        data.air_quality_index = 75.0
        data.save()
        updated_data = AirQualityData.objects.get(pk=data.pk)
        assert updated_data.air_quality_index == 75.0

    # Deleting an AirQualityData instance from the database
    def test_delete_air_quality_data(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        data_pk = data.pk
        data.delete()
        with pytest.raises(AirQualityData.DoesNotExist):
            AirQualityData.objects.get(pk=data_pk)

    # Checking the string representation of an AirQualityData instance
    def test_str_representation_of_air_quality_data(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        expected_str = f"Air Quality Data {data.generated_timestamp} 50.0 Good "
        assert str(data) == expected_str

    # Creating an AirQualityData instance with null values for nullable fields
    def test_create_air_quality_data_with_null_values(self):
        data = AirQualityData.objects.create(
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        assert data.air_quality_index is None
        assert data.air_quality_class is None

    # Creating an AirQualityData instance with maximum length strings for CharField fields
    def test_create_air_quality_data_with_max_length_strings(self):
        max_length_string = "x" * 10
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class=max_length_string,
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning=max_length_string
        )
        assert len(data.air_quality_class) == 10
        assert len(data.air_quality_calibration_meaning) == 10

    # Creating an AirQualityData instance with negative values for FloatField fields
    def test_create_air_quality_data_with_negative_values(self):
        data = AirQualityData.objects.create(
            air_quality_index=-50.0,
            air_quality_class="Poor",
            carbon_dioxide_value=-400.0,
            breath_equivalent_voc=-0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Not Calibrated"
        )
        assert data.air_quality_index == -50.0
        assert data.carbon_dioxide_value == -400.0
        assert data.breath_equivalent_voc == -0.5

    # Creating an AirQualityData instance with zero values for IntegerField fields
    def test_create_air_quality_data_with_zero_values(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Moderate",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=0,
            air_quality_calibration_meaning="Not Calibrated"
        )
        assert data.air_quality_calibration_status == 0

    # Creating an AirQualityData instance with future dates for DateTimeField fields
    def test_create_air_quality_data_with_future_dates(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated",
            generated_timestamp=future_date,
            created_timestamp=future_date
        )
        assert data.generated_timestamp == future_date
        assert data.created_timestamp == future_date

    # Validating the auto_now_add and auto_now properties for DateTimeField fields
    def test_auto_now_add_and_auto_now_properties(self):
        data = AirQualityData.objects.create(
            air_quality_index=50.0,
            air_quality_class="Good",
            carbon_dioxide_value=400.0,
            breath_equivalent_voc=0.5,
            air_quality_calibration_status=1,
            air_quality_calibration_meaning="Calibrated"
        )
        assert data.generated_timestamp is not None
        assert data.created_timestamp is not None
        assert data.modified_timestamp is not None

        old_modified_timestamp = data.modified_timestamp

        data.air_quality_index = 75.0
        data.save()

        assert data.modified_timestamp > old_modified_timestamp

    # Ensuring the air_quality_calibration_status field does not exceed the max length
    def test_air_quality_calibration_status_max_length(self):
        with pytest.raises(ValueError):
            AirQualityData.objects.create(
                air_quality_index=50.0,
                air_quality_class="Good",
                carbon_dioxide_value=400.0,
                breath_equivalent_voc=0.5,
                air_quality_calibration_status=int("9" * 11),
                air_quality_calibration_meaning="Calibrated"
            )


class TestLightData:

    # Create LightData instance with all fields populated
    def test_create_lightdata_all_fields_populated(self):
        light_data = LightData.objects.create(
            light_lux=500.0,
            light_unit='lux',
            white_level_balance=75.0
        )
        assert light_data.light_lux == 500.0
        assert light_data.light_unit == 'lux'
        assert light_data.white_level_balance == 75.0

    # Retrieve LightData instance and verify field values
    def test_retrieve_lightdata_verify_fields(self):
        light_data = LightData.objects.create(
            light_lux=300.0,
            light_unit='lux',
            white_level_balance=50.0
        )
        retrieved = LightData.objects.get(id=light_data.id)
        assert retrieved.light_lux == 300.0
        assert retrieved.light_unit == 'lux'
        assert retrieved.white_level_balance == 50.0

    # Update LightData instance and verify modified_timestamp changes
    def test_update_lightdata_verify_modified_timestamp(self):
        light_data = LightData.objects.create(
            light_lux=200.0,
            light_unit='lux',
            white_level_balance=25.0
        )
        old_timestamp = light_data.modified_timestamp
        light_data.light_lux = 250.0
        light_data.save()
        assert light_data.modified_timestamp > old_timestamp

    # Delete LightData instance and ensure it is removed from the database
    def test_delete_lightdata_instance(self):
        light_data = LightData.objects.create(
            light_lux=100.0,
            light_unit='lux',
            white_level_balance=10.0
        )
        light_data_id = light_data.id
        light_data.delete()
        with pytest.raises(LightData.DoesNotExist):
            LightData.objects.get(id=light_data_id)

    # Verify __str__ method returns the correct string format
    def test_str_method_format(self):
        light_data = LightData.objects.create(
            light_lux=150.0,
            light_unit='lux',
            white_level_balance=20.0
        )
        expected_str = f"Light Data {light_data.generated_timestamp} 150.0 lux "
        assert str(light_data) == expected_str

    # Create LightData instance with null values for all nullable fields
    def test_create_lightdata_null_values(self):
        light_data = LightData.objects.create(
            light_lux=None,
            light_unit=None,
            white_level_balance=None
        )
        assert light_data.light_lux is None
        assert light_data.light_unit is None
        assert light_data.white_level_balance is None

    # Create LightData instance with maximum length for light_unit
    def test_create_lightdata_max_length_light_unit(self):
        max_length_unit = 'x' * 10
        light_data = LightData.objects.create(
            light_lux=100.0,
            light_unit=max_length_unit,
            white_level_balance=10.0
        )
        assert len(light_data.light_unit) == 10

    # Create LightData instance with maximum float value for light_lux and white_level_balance
    def test_create_lightdata_max_float_values(self):
        max_float_value = float('inf')
        light_data = LightData.objects.create(
            light_lux=max_float_value,
            white_level_balance=max_float_value,
            light_unit='lux'
        )
        assert light_data.light_lux == max_float_value
        assert light_data.white_level_balance == max_float_value

    # Create LightData instance with invalid data types for fields
    def test_create_lightdata_invalid_data_types(self):
        with pytest.raises(ValueError):
            LightData.objects.create(
                light_lux='invalid',
                white_level_balance='invalid',
                light_unit=12345
            )

    # Retrieve LightData instance that does not exist
    def test_retrieve_nonexistent_lightdata_instance(self):
        with pytest.raises(LightData.DoesNotExist):
            LightData.objects.get(id=9999)

    # Test auto_now_add for generated_timestamp and created_timestamp
    def test_auto_now_add_timestamps(self):
        import datetime
        before_creation = datetime.datetime.now()
        light_data = LightData.objects.create(
            light_lux=100.0,
            white_level_balance=10.0,
            light_unit='lux'
        )
        after_creation = datetime.datetime.now()
        assert before_creation <= light_data.generated_timestamp <= after_creation
        assert before_creation <= light_data.created_timestamp <= after_creation

    # Test auto_now for modified_timestamp
    def test_auto_now_modified_timestamp(self):
        import datetime
        light_data = LightData.objects.create(
            light_lux=100.0,
            white_level_balance=10.0,
            light_unit='lux'
        )
        before_update = datetime.datetime.now()
        light_data.light_lux = 200.0
        light_data.save()
        after_update = datetime.datetime.now()
        assert before_update <= light_data.modified_timestamp <= after_update


class TestSoundData:

    # Create SoundData instance with all fields populated
    def test_create_instance_all_fields(self):
        sound_data = SoundData.objects.create(
            sound_decibel_SPL_dBA=85.0,
            sound_unit="dBA",
            frequency_band_125=10.0,
            frequency_band_250=20.0,
            frequency_band_500=30.0,
            frequency_band_1000=40.0,
            frequency_band_2000=50.0,
            frequency_band_4000=60.0,
            peak_amp_mPa=70.0,
            stable=1.0
        )
        assert sound_data.sound_decibel_SPL_dBA == 85.0
        assert sound_data.sound_unit == "dBA"

    # Create SoundData instance with only required fields populated
    def test_create_instance_required_fields(self):
        sound_data = SoundData.objects.create()
        assert sound_data is not None

    # Retrieve SoundData instance and verify field values
    def test_retrieve_instance_verify_fields(self):
        sound_data = SoundData.objects.create(sound_decibel_SPL_dBA=85.0, sound_unit="dBA")
        retrieved = SoundData.objects.get(id=sound_data.id)
        assert retrieved.sound_decibel_SPL_dBA == 85.0
        assert retrieved.sound_unit == "dBA"

    # Update SoundData instance and verify modified_timestamp changes
    def test_update_instance_verify_modified_timestamp(self):
        sound_data = SoundData.objects.create(sound_decibel_SPL_dBA=85.0)
        old_timestamp = sound_data.modified_timestamp
        sound_data.sound_decibel_SPL_dBA = 90.0
        sound_data.save()
        assert sound_data.modified_timestamp > old_timestamp

    # Delete SoundData instance and verify it no longer exists
    def test_delete_instance_verify_nonexistence(self):
        sound_data = SoundData.objects.create(sound_decibel_SPL_dBA=85.0)
        sound_data_id = sound_data.id
        sound_data.delete()
        with pytest.raises(SoundData.DoesNotExist):
            SoundData.objects.get(id=sound_data_id)

    # Create SoundData instance with null values for all optional fields
    def test_create_instance_null_optional_fields(self):
        sound_data = SoundData.objects.create()
        assert sound_data.sound_decibel_SPL_dBA is None
        assert sound_data.sound_unit is None

    # Create SoundData instance with maximum length strings for sound_unit
    def test_create_instance_max_length_sound_unit(self):
        max_length_string = "a" * 10
        sound_data = SoundData.objects.create(sound_unit=max_length_string)
        assert sound_data.sound_unit == max_length_string

    # Create SoundData instance with negative values for frequency bands
    def test_create_instance_negative_frequency_bands(self):
        sound_data = SoundData.objects.create(frequency_band_125=-10.0)
        assert sound_data.frequency_band_125 == -10.0

    # Create SoundData instance with zero values for frequency bands
    def test_create_instance_zero_frequency_bands(self):
        sound_data = SoundData.objects.create(frequency_band_125=0.0)
        assert sound_data.frequency_band_125 == 0.0

    # Create SoundData instance with future dates for generated_timestamp
    def test_create_instance_future_generated_timestamp(self):
        future_date = timezone.now() + timedelta(days=1)
        sound_data = SoundData.objects.create(generated_timestamp=future_date)
        assert sound_data.generated_timestamp == future_date

    # Verify __str__ method returns expected string format
    def test_str_method_format(self):
        sound_data = SoundData.objects.create(sound_decibel_SPL_dBA=85.0, sound_unit="dBA")
        expected_str = f"Sound Data {sound_data.generated_timestamp} 85.0 dBA"
        assert str(sound_data) == expected_str

    # Test auto_now_add for generated_timestamp and created_timestamp
    def test_auto_now_add_timestamps(self):
        before_creation = timezone.now()
        sound_data = SoundData.objects.create()
        after_creation = timezone.now()
        assert before_creation <= sound_data.generated_timestamp <= after_creation
        assert before_creation <= sound_data.created_timestamp <= after_creation


class TestParticleData:

    # correctly saves particle data with all fields provided
    def test_saves_particle_data_with_all_fields(self):
        data = ParticleData(
            particle_concentration=10.5,
            particle_concentration_unit='ug/m3',
            particle_duty_cycle_pc=50.0,
            particle_valid=True
        )
        data.save()
        retrieved = ParticleData.objects.get(id=data.id)
        assert retrieved.particle_concentration == 10.5
        assert retrieved.particle_concentration_unit == 'ug/m3'
        assert retrieved.particle_duty_cycle_pc == 50.0
        assert retrieved.particle_valid is True

    # correctly handles missing optional fields
    def test_handles_missing_optional_fields(self):
        data = ParticleData()
        data.save()
        retrieved = ParticleData.objects.get(id=data.id)
        assert retrieved.particle_concentration is None
        assert retrieved.particle_concentration_unit is None
        assert retrieved.particle_duty_cycle_pc is None
        assert retrieved.particle_valid is None

    # auto-generates timestamps on creation
    def test_auto_generates_timestamps_on_creation(self):
        data = ParticleData()
        data.save()
        assert data.generated_timestamp is not None
        assert data.created_timestamp is not None

    # updates modified_timestamp on save
    def test_updates_modified_timestamp_on_save(self):
        data = ParticleData()
        data.save()
        initial_modified_timestamp = data.modified_timestamp
        data.particle_concentration = 20.0
        data.save()
        assert data.modified_timestamp > initial_modified_timestamp

    # correctly handles valid boolean values
    def test_handles_valid_boolean_values(self):
        data = ParticleData(particle_valid=True)
        data.save()
        retrieved = ParticleData.objects.get(id=data.id)
        assert retrieved.particle_valid is True

    # handles extremely large float values
    def test_handles_extremely_large_float_values(self):
        large_value = 1e40
        data = ParticleData(particle_concentration=large_value)
        data.save()
        retrieved = ParticleData.objects.get(id=data.id)
        assert retrieved.particle_concentration == large_value

    # handles extremely small float values
    def test_handles_extremely_small_float_values(self):
        small_value = 1e-40
        data = ParticleData(particle_concentration=small_value)
        data.save()
        retrieved = ParticleData.objects.get(id=data.id)
        assert retrieved.particle_concentration == small_value

    # handles invalid boolean values
    def test_handles_invalid_boolean_values(self):
        with pytest.raises(ValueError):
            ParticleData(particle_valid="not_a_boolean").save()

    # handles invalid date formats
    def test_handles_invalid_date_formats(self):
        with pytest.raises(ValueError):
            ParticleData(generated_timestamp="invalid_date").save()

    # handles null values for non-nullable fields
    def test_handles_null_values_for_non_nullable_fields(self):
        with pytest.raises(ValueError):
            ParticleData(particle_concentration=None).save()

    # validates particle_concentration_unit length
    def test_validates_particle_concentration_unit_length(self):
        with pytest.raises(ValueError):
            ParticleData(particle_concentration_unit='a' * 11).save()

    # validates particle_duty_cycle_pc length
    def test_validates_particle_duty_cycle_pc_length(self):
        with pytest.raises(ValueError):
            ParticleData(particle_duty_cycle_pc='a' * 11).save()
