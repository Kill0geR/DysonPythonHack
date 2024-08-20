# DysonPythonHack

DysonPythonHack is a library which allows users to control their dyson fans.

---
# How does DysonPythonHack work?

This how you use the Library when you now the IP-Address of your dyson

````python
from DysonPythonHack import DysonDevice

DYSON_IP = "192.168.1.1"
DYSON_SSID = "NN2-EU-########"
DYSON_PASSWORD = "#######"

connect_dyson = DysonDevice(DYSON_IP, DYSON_SSID, DYSON_PASSWORD)
connect_dyson.start(speed=5, rotation=True, night_mode=False, fan_mode=True)
````

---
This how you use the Library when you **DON'T** now the IP-Address of your dyson

````python
from DysonPythonHack import DysonDevice
from DysonPythonHack import DysonIP
import os

DYSON_IP = DysonIP().auto_ip_addr_dyson()
DYSON_SSID = "NN2-EU-########"
DYSON_PASSWORD = "#######"

if not DYSON_IP:
    print("Failed to find Dyson IP")
    os._exit(0)

connect_dyson = DysonDevice(DYSON_IP, DYSON_SSID, DYSON_PASSWORD)
connect_dyson.start(speed=5, rotation=True, night_mode=False, fan_mode=True)
````

---
# Parameter meanings
* speed: You can set the speed between 1 and 10
* rotation: If you set rotation to True your Fan will rotate
* night_mode: If you set night_mode to True your Fan will enter the Night mode 
* fan_mod: If you set fan_mode to True your Fan will turn on
