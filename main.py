from DysonPythonHack import DysonDevice
from DysonPythonHack import DysonIP

DYSON_IP = DysonIP().auto_ip_addr_dyson()
DYSON_SSID = "NN2-EU-########"
DYSON_PASSWORD = "#######"

if not DYSON_IP:
    print("Failed to find Dyson IP")
    os._exit(0)

print(f"Dyson IP: {DYSON_IP}")

connect_dyson = DysonDevice(DYSON_IP, DYSON_SSID, DYSON_PASSWORD)
connect_dyson.start(speed=5, rotation=True, night_mode=False, fan_mode=True)