# Example of how to use BTHome beacons with aioble in MicroPython
# Some parts are ESP32 specific, but most code is portable.

from machine import deepsleep, unique_id
from binascii import hexlify
import asyncio
import aioble
import bthome

BLE_ADV_INTERVAL_uS = 250000
AWAKE_TIME_SECS = 60   # How long to spend advertising and servicing clients.
SLEEP_TIME_SECS = 120  # How long to spend in deep sleep.

base_mac = unique_id()  # WiFi MAC
bluetooth_mac = bytearray(base_mac)
bluetooth_mac[5] += 2   # ESP32 Bluetooth MAC is always WiFi MAC + 2

bthome.device_name = "DIY-sensor"
print(bthome.device_name)
print(hexlify(bluetooth_mac, ':').decode().upper())

async def read_sensor():
    bthome.temperature = 25  # Mocked up data for testing purposes.
    bthome.humidity = 50.55
    await asyncio.sleep(AWAKE_TIME_SECS)
    print("Going to sleep.")
    deepsleep(SLEEP_TIME_SECS * 1000)  # Helps mitigate sensor self-heating.

async def communicate_readings():
    print("Constructing advertising payload")
    while True:
        async with await aioble.advertise(
            BLE_ADV_INTERVAL_uS,
            adv_data = bthome.pack_advertisement(bthome.TEMPERATURE_SINT16, bthome.HUMIDITY_UINT16)
        ) as connection:
            print("Client connect:", connection.device)
            await connection.disconnected(timeout_ms=None)
            print("Client disconnect.")


async def main():
    task1 = asyncio.create_task(read_sensor())
    task2 = asyncio.create_task(communicate_readings())
    await asyncio.gather(task1, task2)

asyncio.run(main())
