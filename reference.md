# BTHome v2 Advertising Payload for MicroPython

The BTHome v2 format reference is published at https://bthome.io/format/. This document will distill the format into a blueprint for MicroPython code.

Given the following sample BTHome advertising payload:

```
020106 0B094449592D73656E736F72 0A16D2FC4002C40903BF13
```

The advertisement is one continuous string of hex digits, but is separated into three distint parts using spaces for ease of reading. These parts are:

1. Flags
2. Local Name
3. Service Data

## Advertisement Flags

The first part contains Bluetooth flags. It is always the same for any BTHome advertisements.

```
020106
```

* 02 is the length byte
* 01 is an indicator for flags
* 06 is flag data (0b00000110)
  * bit 1: LE General Discoverable Mode
  * bit 2: BR/EDR Not Supported

Because it never changes, flags can be represented as a static bytestring.

```
BTHOME_FLAGS = bytes.fromhex('020106')
```

## Device Name

The second part contains the name of the device encoded as ASCII with bytes prepended to indicate name length and type.

```
0B094449592D73656E736F72
```

* 0B is the length byte (does not include the length byte itself in calculations, but does inslude the type indicator for complete or shortened)
* 09 is an indicator for complete name (as opposed to shortened name being 0x08)
* 4449592D73656E736F72 ASCII encoded hex string reading "DIY-sensor"

The device name should be user defined and flexible in length. But, it is competing for the small space available for advertising data. Ten bytes (the same as used by the example name "DIY-sensor" seems to be a reasonable limit.

See https://stackoverflow.com/questions/65568893/how-to-know-the-maximum-length-of-bt-name#65577574 for a good discussion of this limit.

Because the name is user definded and may vary in length, it will be provided as a string and:
* The string length must be non-zero and not exceeding maximum length
* The string must be converted to ASCII-encoded bytes
* The length of the string must be calculated
* The complete name indicator (0x09) must be prepended to the byte string.
* The length of the string (including the "complete name" indicator) must be calculated and prepended to the final byte string.


## Service Data

The third part is service data. It contains the information to indicate a BTHome advertisement as well as values gathered from various sensors.

```
0A16D2FC4002C40903BF13
```

* 0A is the length byte
* 16 indicates a service data type of UUID16 follows
* D2FC is the UUID16 indicating BTHome data follows (little endian format for FCD2, the UUID16 reserved for BTHome)
* 40 is flag data
  * bit 0: encrypted
  * bit 1: reserved
  * bit 2: trigger based (irregular advertisement triggered by some user interaction)
  * bit 3: reserved
  * bit 4: reserved
  * bits 5..7: BTHome version (010 for version 2)
* 02C40903BF13 represents sensor data
  * 02 indicates temperature measurement
  * C409 is 25 C temperature in little endian format with a two-place fixed-point decimal (similar to GATT characteristic)
  * 03 indicates humidity measurement
  * BF13 is 50.55% humidity in little endian with a two-place fixed-point decimal (similar to GATT characteristic)

Additional sensor types and value may be found under the heading of "sensor data" on https://bthome.io/format/

Because an arbitrary number of zero or more sensors can be configured, the byte string should start as 16D2FC (UUID16 indicator and BTHome UUID.)
* Flag data should be 0x00 for regular interval devices or 0x40 for triggered devices.
  * Encryption will remain unimplemented at this time, so the bit 0 will be 0.
  * Sensors configured to send updates at regular intervals should have a bit 2 of 0, triggered advertisements have a bit 2 of 1.
* Sensor readings should be put into proper format and appended.
  * Each reading starts with a one-byte object ID to indicate the type
  * Reading values are always little endian
  * Non-integer values used fix-point decimal (often two decimal places)
  * Length of values can vary between one to three bytes depending on object ID

`struct.pack()` is helpful in converting object ID and value to little endian bytes. 24-bit values pose a challenge because there is no format string for a 3-byte value available to `struct.pack()`. This can be overcome by using a 32-bit long int (L) format and removing the final 0x00 byte.

Examples for encoding environmental data include the following:

```
temperature_bytes = pack('<Bh', BTHOME_TEMPERATURE_SINT16, temperature_celsius * 100)
humidity_bytes = pack('<Bh', BTHOME_HUMIDITY_UINT16, round(humidity_percent * 100))
illuminance_bytes = pack('<BL', BTHOME_ILLUMINANCE_UINT24, illuminance_lux)[:-1]
```
