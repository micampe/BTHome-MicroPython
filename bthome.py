# BTHome MicroPython
# Construct Bluetooth Low Energy (BLE) advertising payloads for BTHome v2.
# See https://bthome.io/ for more information about BTHome.
# See https://github.com/DavesCodeMusings/BTHome-MicroPython for more about this module.

from micropython import const
from struct import pack

# See "Advertising Payload" at https://bthome.io/format/ for details.
_ADVERT_LENGTH_MAX = const(255)
_ADVERT_FLAGS = bytes.fromhex('020106')  # length (02), flags indicator (01), flag bits (06)
_DEVICE_NAME_LENGTH_MAX = const(10)
_SERVICE_DATA_UUID16 = const(0x16)
_SERVICE_UUID16 = const(0xFCD2)   # See: https://bthome.io/images/License_Statement_-_BTHOME.pdf
_DEVICE_INFO_FLAGS = const(0x40)  # Currently hardcoded: no encryption, regular updates, version 2

# See "Sensor Data" table at https://bthome.io/format/ for details.
BATTERY_UINT8 = const(0x01)
TEMPERATURE_SINT16 = const(0x02)
_TEMPERATURE_SINT16_SCALING = const(100)
HUMIDITY_UINT16 = const(0x03)
_HUMIDITY_UINT16_SCALING = const(100)
PRESSURE_UINT24 = const(0x04)
_PRESSURE_UINT24_SCALING = const(100)
ILLUMINANCE_UINT24 = const(0x05)
_ILLUMINANCE_UINT24_SCALING = const(100)

# Default value decimal places indicate precision
device_name = "BTHome-MPY"
battery = 0         # percent
temperature = 0.00  # degrees Celsius
humidity = 0.00     # percent (relative humidity)
pressure = 0.00     # hectoPascals (millibars)
illuminance = 0.0   # Lux

def _pack_device_name():
    assert len(device_name) > 0
    assert len(device_name) <= _DEVICE_NAME_LENGTH_MAX
    name_type = bytes.fromhex('09')  # indicator for complete name
    device_name_bytes = name_type + device_name.encode()
    device_name_bytes = bytes([len(device_name_bytes)]) + device_name_bytes
    return device_name_bytes

# Functions to conver integer or float values to little endian fixed-point decimal
def _pack_battery():
    return pack('BB', BATTERY_UINT8, battery)

def _pack_temperature(object_id):
    if object_id == TEMPERATURE_SINT16:
        temperature_bytes = pack('<Bh', TEMPERATURE_SINT16, round(temperature * _TEMPERATURE_SINT16_SCALING))
    else:
        temperature_bytes = bytes()
    return temperature_bytes

def _pack_humidity(object_id):
    if object_id == HUMIDITY_UINT16:
        humidity_bytes = pack('<Bh', HUMIDITY_UINT16, round(humidity * _HUMIDITY_UINT16_SCALING))
    else:
        humidity_bytes = bytes()
    return humidity_bytes

def _pack_pressure(object_id):
    if object_id == PRESSURE_UINT24:
        pressure_bytes = pack('<BL', PRESSURE_UINT24, round(pressure * _PRESSURE_UINT24_SCALING))[:-1]
    else:
        pressure_bytes = bytes()
    return pressure_bytes

def _pack_illuminance(object_id):
    if object_id == ILLUMINANCE_UINT24:
        illuminance_bytes = pack('<BL', ILLUMINANCE_UINT24, round(illuminance * _ILLUMINANCE_UINT24_SCALING))[:-1]
    else:
        illuminance_bytes = bytes()
    return illuminance_bytes

# Concatenate an arbitrary number of sensor readings using parameters of sensor data constants to indicate what's included.
def _pack_service_data(*args):
    service_data_bytes = pack('B', _SERVICE_DATA_UUID16)  # indicates a 16-bit service UUID follows
    service_data_bytes += pack('<h', _SERVICE_UUID16)
    service_data_bytes += pack('B', _DEVICE_INFO_FLAGS)
    for object_id in args:
        if object_id == BATTERY_UINT8:
            service_data_bytes += _pack_battery()
        if object_id == TEMPERATURE_SINT16:
            service_data_bytes += _pack_temperature(TEMPERATURE_SINT16)
        if object_id == HUMIDITY_UINT16:
            service_data_bytes += _pack_humidity(HUMIDITY_UINT16)
        if object_id == PRESSURE_UINT24:
            service_data_bytes += _pack_pressure(PRESSURE_UINT24)
        if object_id == ILLUMINANCE_UINT24:
            service_data_bytes += _pack_illuminance(ILLUMINANCE_UINT24)
    service_data_bytes = pack('B', len(service_data_bytes)) + service_data_bytes
    return service_data_bytes

# Construct advertising payload suitable for use by MicroPython's aioble.advertise(adv_data)
def pack_advertisement(*args):
    advertisement_bytes = _ADVERT_FLAGS  # All BTHome adverts start this way.
    advertisement_bytes += _pack_device_name()
    advertisement_bytes += _pack_service_data(*args)
    assert len(advertisement_bytes) < _ADVERT_LENGTH_MAX
    return advertisement_bytes
