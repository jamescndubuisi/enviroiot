import time
from datetime import datetime
import sensor_package.servers as server
import sensor_package.sensor_functions as sensor
import sensor_package.sensor_constants as const
import requests

cycle_period = const.CYCLE_PERIOD_3_S
SERVER_PORT = 8000
SERVER_NAME = "www.wonderlusts.org/enviroiot"
API_KEY = ""


(GPIO, I2C_bus) = sensor.SensorHardwareSetup()

# Apply the chosen settings to the MS430
I2C_bus.write_i2c_block_data(
    sensor.i2c_7bit_address,
    const.PARTICLE_SENSOR_SELECT_REG, [sensor.PARTICLE_SENSOR])
I2C_bus.write_i2c_block_data(
    sensor.i2c_7bit_address, const.CYCLE_TIME_PERIOD_REG, [cycle_period])

# Set the automatic refresh period of the web page. It should refresh
# at least as often as new data are obtained. A more frequent refresh is
# best for long cycle periods because the page access will be
# out-of-step with the cycle. Users can also manually refresh the page.
if cycle_period == const.CYCLE_PERIOD_3_S:
    server.SimpleWebpageHandler.refresh_period_seconds = 3
elif cycle_period == const.CYCLE_PERIOD_100_S:
    server.SimpleWebpageHandler.refresh_period_seconds = 30
else:  # CYCLE_PERIOD_300_S
    server.SimpleWebpageHandler.refresh_period_seconds = 50

# Choose the TCP port number for the web page.
port = 8080
# The port can be any unused number from 1-65535 but values below 1024
# require this program to be run as super-user as follows:
#    sudo python3 web_server.py
# Port 80 is the default for HTTP, and with this value the port number
# can be omitted from the web address. e.g. http://172.24.1.1

print("Connecting to Web server or IP address...")


# Enter cycle mode to start periodic data output
I2C_bus.write_byte(sensor.i2c_7bit_address, const.CYCLE_MODE_CMD)

while True:

    # While waiting for the next data release, respond to client requests
    # by serving the web page with the last available data.
    while not GPIO.event_detected(sensor.READY_pin):
        time.sleep(0.05)

    # Now read all data from the MS430 and pass to the web page

    # Air data
    air_data = sensor.get_air_data(I2C_bus)

    # Air quality data
    # The initial self-calibration of the air quality data may take several
    # minutes to complete. During this time the accuracy parameter is zero
    # and the data values are not valid.
    air_quality_data = sensor.get_air_quality_data(I2C_bus)

    # Light data
    light_data = sensor.get_light_data(I2C_bus)

    # Sound data
    sound_data = sensor.get_sound_data(I2C_bus)

    # Particle data
    # This requires the connection of a particulate sensor (invalid
    # values will be obtained if this sensor is not present).
    # Also note that, due to the low pass filtering used, the
    # particle data become valid after an initial initialization
    # period of approximately one minute.
    particle_data = None
    if sensor.PARTICLE_SENSOR != const.PARTICLE_SENSOR_OFF:
        particle_data = sensor.get_particle_data(I2C_bus, sensor.PARTICLE_SENSOR)

    # Create the updated web page ready for client requests, passing
    # the current date and time for displaying with the data
    data = (f'{datetime.now():%H:%M:%S %Y-%m-%d}',air_data, air_quality_data, light_data, sound_data, particle_data)
    send_data = requests.post(
        f'http://{SERVER_NAME}:{SERVER_PORT}/', data=data, api_key=API_KEY)
    # server.SimpleWebpageHandler.assemble_web_page(
    #     f'{datetime.now():%H:%M:%S %Y-%m-%d}')
