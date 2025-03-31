# Example of how to use BTHome beacons with aioble in MicroPython
# Some parts are ESP32 specific, but most code is portable.

from machine import Pin, deepsleep
import asyncio
import aioble
from bthome import BTHome

BLE_ADV_INTERVAL_uS = 250000
AWAKE_TIME_SECS = 60  # How long to spend advertising and servicing clients.
SLEEP_TIME_SECS = 120  # How long to spend in deep sleep.
STATUS_LED_GPIO = 2  # Light while awake and advertising.

status = Pin(STATUS_LED_GPIO, Pin.OUT)
beacon = BTHome("DIY-sensor", debug=True)


async def read_sensor():
    status.on()
    beacon.temperature = 25  # Mocked up data for testing purposes.
    beacon.humidity = 50.55
    await asyncio.sleep(AWAKE_TIME_SECS)
    print("Going to sleep.")
    status.off()
    deepsleep(SLEEP_TIME_SECS * 1000)  # Helps mitigate sensor self-heating.


async def communicate_readings():
    print("Constructing advertising payload")
    bthome_advert = beacon.pack_advertisement(
        BTHome.TEMPERATURE_SINT16_X100, BTHome.HUMIDITY_UINT16_X100
    )
    await aioble.advertise(
        BLE_ADV_INTERVAL_uS,
        adv_data=bthome_advert,
        connectable=False,
    )


async def main():
    task1 = asyncio.create_task(read_sensor())
    task2 = asyncio.create_task(communicate_readings())
    await asyncio.gather(task1, task2)


asyncio.run(main())
