import requests

# data = {'SPL_dBA': 69.3, 'SPL_bands_dB': [60.0, 64.3, 67.4, 61.9, 61.3, 58.4], 'peak_amp_mPa': 533.25, 'stable': 0}


def convert_sound_data(data):
    frequency_bands = {
      'frequency_band_125': data['SPL_bands_dB'][0],
      'frequency_band_250': data['SPL_bands_dB'][1],
      'frequency_band_500': data['SPL_bands_dB'][2],
      'frequency_band_1000': data['SPL_bands_dB'][3],
      'frequency_band_2000': data['SPL_bands_dB'][4],
      'frequency_band_4000': data['SPL_bands_dB'][5]
    }

    new_data = {
      'sound_decibel_SPL_dBA': data['SPL_dBA'],
      'peak_amp_mPa': data['peak_amp_mPa'],
      'stable': data['stable'],
    }
    new_data.update(frequency_bands)
    return new_data


def convert_particle_data(data):
    new_data = {
        'particle_concentration': data['concentration'],
        'particle_duty_cycle_pc': data['duty_cycle_pc'],
        'particle_valid': data['valid'],
    }
    return new_data


def convert_light_data(data):
    new_data = {
      'light_lux': data['illum_lux'],
      'white_level_balance': data['white']
    }
    return new_data


def convert_air_data(data):
  new_data = {
      'temperature_celsius': data['T_C'],
      'pressure_value': data['P_Pa'],
      'humidity_value': data['H_pc'],
      'gas_sensor_resistance': data['G_ohm'],
      'temperature_fahrenheit': data['T_F'],
      'temperature_unit': data['T_unit'],
      'temperature_value': data['T']
  }
  return new_data


def convert_air_quality_data(data):
  """Converts the input data dictionary to the desired format.

  Args:
    data: The input data dictionary.

  Returns:
    The converted data dictionary.
  """

  new_data = {
      'air_quality_index': data['AQI'],
      'carbon_dioxide_value': data['CO2e'],
      'breath_equivalent_voc': data['bVOC'],
      'air_quality_calibration_status': data['AQI_accuracy']
  }
  return new_data


# API endpoint URL
api_url = 'http://localhost:8000/api/'

# Token for authentication
token = 'edb34767f9a38ab8dbea306a3c9dd8c016204adb'
# Headers for the request, including the Authorization header with the token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}


def send_air_quality_data(url="air-quality-data/", data=None):
    # Data to be sent in the POST request

    if data:
        data = convert_air_quality_data(data)
    else:
        print("No data received. Sending default data")
        data = {
            'air_quality_index': 100,
            'carbon_dioxide_value': 400,
            'breath_equivalent_voc': 20,
            'air_quality_calibration_status': 1
        }

    # Make the POST request
    response = requests.post(api_url+url, json=data, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.json())

    return response


def send_air_data(url="air-data/", data=None):
    # Data to be sent in the POST request

    if data:
        data = convert_air_data(data)
    else:
        print("No data received. Sending default data")
        data = {
            'temperature_celsius': 23.7,
            'pressure_value': 14400,
            'humidity_value': 80,
            'gas_sensor_resistance': 29890,
            'temperature_fahrenheit': 74.66,
            'temperature_unit': '°C',
            'temperature_value': 23.7
        }

    # Make the POST request
    response = requests.post(api_url+url, json=data, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.json())

    return response


def send_sound_data(url="sound-data/", data=None):
    # Data to be sent in the POST request
    if data:
        data = convert_sound_data(data)
    else:
        print("No data recieved, Sending default data")

        data = {
            'sound_decibel_SPL_dBA': 23.7,
            'peak_amp_mPa': 5.90,
            'stable': 1, # boolean
            'frequency_band_125': 13.9,
            'frequency_band_250': 64.66,
            'frequency_band_500': 54.66,
            'frequency_band_1000': 44.66,
            'frequency_band_2000': 34.66,
            'frequency_band_4000': 23.8,

        }

    # Make the POST request
    response = requests.post(api_url+url, json=data, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.json())

    return response


def send_particle_data(url="particle-data/", data=None):

    if data:
        data = convert_particle_data(data)
    else:
        print("No data received. Sending default data")
        # Data to be sent in the POST request
        data = {
            'particle_concentration': 23.7,
            'particle_duty_cycle_pc': 5.90,
            'particle_valid': 1, # boolean


        }

    # Make the POST request
    response = requests.post(api_url+url, json=data, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.json())

    return response


def send_light_data(url="light-data/"):
    # Data to be sent in the POST request
    data = {
        'light_lux': 23.7,
        'white_level_balance': 5.90,


    }

    # Make the POST request
    response = requests.post(api_url+url, json=data, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.json())

    return response
# outputaqd = send_air_quality_data()
# outputad = send_air_data()
# outputsd = send_sound_data()
# outputld = send_light_data()


# outputpd = send_particle_data()



