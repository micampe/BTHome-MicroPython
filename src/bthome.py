# BTHome MicroPython
# Construct Bluetooth Low Energy (BLE) advertising payloads for BTHome v2.
# See https://bthome.io for more about how BTHome communicates data.
# See https://github.com/DavesCodeMusings/BTHome-MicroPython for more about this module.
# Other interesting references are given as footnotes (e.g. [^1])

from micropython import const
from struct import pack


class BTHome:
    # Bluetooth Low Energy flags
    _ADVERT_FLAGS = bytes.fromhex(
        "020106"
    )  # length (02), flags indicator (01), flag bits (06) [^1]
    _SERVICE_DATA_UUID16 = 0x16
    _SERVICE_UUID16 = 0xFCD2  # 16-bit UUID reserved for BTHome. [^2]

    # BTHome specific flags
    _DEVICE_INFO_FLAGS = (
        0x40  # Currently hardcoded as: no encryption, regular updates, version 2
    )

    debug = False

    # Device name used in BLE advertisements.
    _local_name = ""

    # See "Sensor Data" table at https://bthome.io/format/ Object ID column.
    BATTERY_UINT8_X1 = const(0x01)  # %
    TEMPERATURE_SINT16_X100 = const(0x02)  # °C
    HUMIDITY_UINT16_X100 = const(0x03)  # %
    PRESSURE_UINT24_X100 = const(0x04)  # hPa
    ILLUMINANCE_UINT24_X100 = const(0x05)  # lux
    MASS_KG_UINT16_X100 = const(0x06)  # kg
    MASS_LB_UINT16_X100 = const(0x07)  # lb
    DEWPOINT_SINT16_X100 = const(0x08)  # °C
    COUNT_UINT8_X1 = const(0x09)
    ENERGY_UINT24_X1000 = const(0x0A)  # kWh
    POWER_UINT24_X100 = const(0x0B)  # W
    VOLTAGE_UINT16_X1000 = const(0x0C)  # V
    PM2_5_UINT16_X1 = const(0x0D)  # ug/m3
    PM10_UINT16_X1 = const(0x0E)  # ug/m3
    CO2_UINT16_X1 = const(0x12)  # ppm
    TVOC_UINT16_X1 = const(0x13)  # ug/m3
    MOISTURE_UINT16_X100 = const(0x14)  # %
    HUMIDITY_UINT8_X1 = const(0x2E)  # %
    MOISTURE_UINT8_X1 = const(0x2F)  # %
    COUNT_UINT16_X1 = const(0x3D)
    COUNT_UINT32_X1 = const(0x3E)
    ROTATION_SINT16_X10 = const(0x3F)  # °
    DISTANCE_MM_UINT16_X1 = const(0x40)  # mm
    DISTANCE_M_UINT16_X10 = const(0x41)  # m
    DURATION_UINT24_X1000 = const(0x42)  # s
    CURRENT_UINT16_X1000 = const(0x43)  # A
    SPEED_UINT16_X100 = const(0x44)  # m/s
    TEMPERATURE_SINT16_X10 = const(0x45)  # °C
    UV_INDEX_UINT8_X10 = const(0x46)
    VOLUME_L_UINT16_X10 = const(0x47)  # L
    VOLUME_ML_UINT16_X1 = const(0x48)  # mL
    VOLUME_FLOW_RATE_X1000 = const(0x49)  # m3/hr
    VOLTAGE_UINT16_X10 = const(0x4A)  # V
    GAS_UINT24_X1000 = const(0x4B)  # m3
    GAS_UINT32_X1000 = const(0x4C)  # m3
    ENERGY_UINT32_X1000 = const(0x4D)  # kWh
    VOLUME_UINT32_X1000 = const(0x4E)  # L
    WATER_UINT32_X1000 = const(0x4F)  # L

    # There is more than one way to represent most sensor properties. This
    # dictionary maps the object id to the property name.
    _object_id_properties = {
        BATTERY_UINT8_X1: "battery",
        TEMPERATURE_SINT16_X100: "temperature",
        HUMIDITY_UINT16_X100: "humidity",
        PRESSURE_UINT24_X100: "pressure",
        ILLUMINANCE_UINT24_X100: "illuminance",
        MASS_KG_UINT16_X100: "mass",
        MASS_LB_UINT16_X100: "mass",
        DEWPOINT_SINT16_X100: "dewpoint",
        COUNT_UINT8_X1: "count",
        ENERGY_UINT24_X1000: "energy",
        POWER_UINT24_X100: "power",
        VOLTAGE_UINT16_X1000: "voltage",
        PM2_5_UINT16_X1: "pm2.5",
        PM10_UINT16_X1: "pm10",
        CO2_UINT16_X1: "co2",
        TVOC_UINT16_X1: "tvoc",
        MOISTURE_UINT16_X100: "moisture",
        HUMIDITY_UINT8_X1: "humidity",
        MOISTURE_UINT8_X1: "moisture",
        COUNT_UINT16_X1: "count",
        COUNT_UINT32_X1: "count",
        ROTATION_SINT16_X10: "rotation",
        DISTANCE_MM_UINT16_X1: "distance",
        DISTANCE_M_UINT16_X10: "distance",
        DURATION_UINT24_X1000: "duration",
        CURRENT_UINT16_X1000: "current",
        TEMPERATURE_SINT16_X10: "temperature",
        UV_INDEX_UINT8_X10: "uv_index",
        VOLUME_L_UINT16_X10: "volume",
        VOLUME_ML_UINT16_X1: "volume",
        VOLUME_FLOW_RATE_X1000: "volume_flow_rate",
        VOLTAGE_UINT16_X10: "voltage",
        GAS_UINT24_X1000: "gas",
        GAS_UINT32_X1000: "gas",
        ENERGY_UINT32_X1000: "energy",
        VOLUME_UINT32_X1000: "volume",
        WATER_UINT32_X1000: "water"
    }

    # Properties below are updated externally when sensor values are read.
    # See "Sensor Data" table at https://bthome.io/format/ Property column.
    acceleration = 0
    battery = 0
    channel = 0
    co2 = 0
    conductivity = 0
    count = 0
    current = 0
    dewpoint = 0
    direction = 0
    distance = 0
    duration = 0
    energy = 0
    gas = 0
    gyroscope = 0
    humidity = 0
    illuminance = 0
    mass = 0
    moisture = 0
    pm10 = 0
    pm2_5 = 0
    power = 0
    precipitation = 0
    pressure = 0
    raw = 0
    rotation = 0
    speed = 0
    temperature = 0
    text = ""
    timestamp = 0
    tvoc = 0
    uv_index = 0
    voltage = 0
    volume = 0
    volume_flow_rate = 0
    volume_storage = 0
    water = 0

    def __init__(self, local_name="BTHome", debug=False):
        local_name = local_name[:10]  # Truncate to fit [^3]
        self._local_name = local_name
        self.debug = debug

    @property
    def local_name(self):
        return self._local_name

    def pack_local_name(self):
        name_type = bytes.fromhex("09")  # indicator for complete name
        local_name_bytes = name_type + self._local_name.encode()
        local_name_bytes = bytes([len(local_name_bytes)]) + local_name_bytes
        if self.debug:
            print("Local name:", self._local_name)
            print("Packed representation:", local_name_bytes.hex().upper())
        return local_name_bytes

    # Technically, the functions below could be static methods, but @staticmethod
    # on a dictionary of functions only works with Python >3.10, and MicroPython
    # is based on 3.4. Also, __func__ and __get()__ workarounds throw errors in
    # MicroPython. [^4]

    # 8-bit unsigned integer with scaling of 1 (no decimal places)
    def _pack_uint8_x1(self, object_id, value):
        return pack("BB", object_id, value)

    # 8-bit unsigned integer with scaling of 10 (1 decimal place)
    def _pack_uint8_x10(self, object_id, value):
        return pack("BB", object_id, value * 10)

    # 16-bit signed integer with scalling of 10 (1 decimal place)
    def _pack_sint16_x10(self, object_id, value):
        return pack("<Bh", object_id, round(value * 10))

    # 16-bit signed integer with scalling of 100 (2 decimal places)
    def _pack_sint16_x100(self, object_id, value):
        return pack("<Bh", object_id, round(value * 100))

    # 16-bit unsigned integer with scalling of 1 (no decimal places)
    def _pack_uint16_x1(self, object_id, value):
        return pack("<BH", object_id, round(value))

    # 16-bit unsigned integer with scalling of 10 (1 decimal place)
    def _pack_uint16_x10(self, object_id, value):
        return pack("<BH", object_id, round(value * 10))

    # 16-bit unsigned integer with scalling of 100 (2 decimal places)
    def _pack_uint16_x100(self, object_id, value):
        return pack("<BH", object_id, round(value * 100))

    # 16-bit unsigned integer with scalling of 1000 (3 decimal places)
    def _pack_uint16_x1000(self, object_id, value):
        return pack("<BH", object_id, round(value * 1000))

    # 24-bit unsigned integer with scaling of 100 (2 decimal places)
    def _pack_uint24_x100(self, object_id, value):
        return pack("<BL", object_id, round(value * 100))[:-1]

    # 24-bit unsigned integer with scaling of 1000 (3 decimal places)
    def _pack_uint24_x1000(self, object_id, value):
        return pack("<BL", object_id, round(value * 1000))[:-1]

    # 32-bit unsigned integer with scaling of 1 (no decimal places)
    def _pack_uint32_x1(self, object_id, value):
        return pack("<BL", object_id, round(value))

    # 32-bit unsigned integer with scaling of 1000 (3 decimal places)
    def _pack_uint32_x1000(self, object_id, value):
        return pack("<BL", object_id, round(value * 1000))

    _object_id_functions = {
        BATTERY_UINT8_X1: _pack_uint8_x1,
        TEMPERATURE_SINT16_X100: _pack_sint16_x100,
        HUMIDITY_UINT16_X100: _pack_uint16_x100,
        PRESSURE_UINT24_X100: _pack_uint24_x100,
        ILLUMINANCE_UINT24_X100: _pack_uint24_x100,
        MASS_KG_UINT16_X100: _pack_uint16_x100,
        MASS_LB_UINT16_X100: _pack_uint16_x100,
        DEWPOINT_SINT16_X100: _pack_sint16_x100,
        COUNT_UINT8_X1: _pack_uint8_x1,
        ENERGY_UINT24_X1000: _pack_uint24_x1000,
        POWER_UINT24_X100: _pack_uint24_x100,
        VOLTAGE_UINT16_X1000: _pack_uint16_x1000,
        PM2_5_UINT16_X1: _pack_uint16_x1,
        PM10_UINT16_X1: _pack_uint16_x1,
        CO2_UINT16_X1: _pack_uint16_x1,
        TVOC_UINT16_X1: _pack_uint16_x1,
        MOISTURE_UINT16_X100: _pack_uint16_x100,
        HUMIDITY_UINT8_X1: _pack_uint8_x1,
        MOISTURE_UINT8_X1: _pack_uint8_x1,
        COUNT_UINT16_X1: _pack_uint16_x1,
        COUNT_UINT32_X1: _pack_uint32_x1,
        ROTATION_SINT16_X10: _pack_sint16_x10,
        DISTANCE_MM_UINT16_X1: _pack_uint16_x1,
        DISTANCE_M_UINT16_X10: _pack_uint16_x10,
        DURATION_UINT24_X1000: _pack_uint24_x1000,
        CURRENT_UINT16_X1000: _pack_uint16_x1000,
        SPEED_UINT16_X100: _pack_sint16_x100,
        TEMPERATURE_SINT16_X10: _pack_sint16_x10,
        UV_INDEX_UINT8_X10: _pack_uint8_x10,
        VOLUME_L_UINT16_X10: _pack_uint16_x10,
        VOLUME_ML_UINT16_X1: _pack_uint16_x1,
        VOLUME_FLOW_RATE_X1000: _pack_uint16_x1000,
        VOLTAGE_UINT16_X10: _pack_uint16_x10,
        GAS_UINT24_X1000: _pack_uint24_x1000,
        GAS_UINT32_X1000: _pack_uint32_x1000,
        ENERGY_UINT32_X1000: _pack_uint32_x1000,
        VOLUME_UINT32_X1000: _pack_uint32_x1000,
        WATER_UINT32_X1000: _pack_uint32_x1000
    }

    # Concatenate an arbitrary number of sensor readings using parameters
    # of sensor data constants to indicate what's to be included.
    def _pack_service_data(self, *args):
        service_data_bytes = pack(
            "B", BTHome._SERVICE_DATA_UUID16
        )  # indicates a 16-bit service UUID follows
        service_data_bytes += pack("<H", BTHome._SERVICE_UUID16)
        service_data_bytes += pack("B", BTHome._DEVICE_INFO_FLAGS)
        for object_id in args:
            func = BTHome._object_id_functions[object_id]
            property = BTHome._object_id_properties[object_id]
            value = getattr(self, property)
            packed_representation = func(self, object_id, value)
            if self.debug:
                print("Using function:", func)
                print("Data property:", property)
                print("Data value:", value)
                print("Packed representation:", packed_representation.hex().upper())
            service_data_bytes += packed_representation
        service_data_bytes = pack("B", len(service_data_bytes)) + service_data_bytes
        return service_data_bytes

    def pack_advertisement(self, *args):
        advertisement_bytes = self._ADVERT_FLAGS  # All BTHome adverts start this way.
        advertisement_bytes += self.pack_local_name()
        advertisement_bytes += self._pack_service_data(*args)
        if self.debug:
            print("BLE Advertisement:", advertisement_bytes.hex().upper())
        return advertisement_bytes


# This demo's values match what is used by the example at: https://bthome.io/format
# The advertisement printed here should match the example BTHome payload.
def demo():
    beacon = BTHome("DIY-sensor", debug=True)
    beacon.temperature = 25
    beacon.humidity = 50.55
    ble_advert = beacon.pack_advertisement(
        BTHome.TEMPERATURE_SINT16_X100, BTHome.HUMIDITY_UINT16_X100
    )
    return ble_advert


if __name__ == "__main__":
    demo()


# [^1]: https://community.silabs.com/s/article/kba-bt-0201-bluetooth-advertising-data-basics
# [^2]: https://bthome.io/images/License_Statement_-_BTHOME.pdf
# [^3]: https://community.st.com/t5/stm32-mcus-wireless/ble-name-advertising/m-p/254711/highlight/true#M10645
# [^4]: https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable
