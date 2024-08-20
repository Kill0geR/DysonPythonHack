import sys
import paho.mqtt.client as mqtt
import base64
import hashlib
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import BetterPrinting as bp


class DysonDevice:
    def __init__(self, dyson_ip, dyson_ssid, dyson_password, dyson_type="475", port=1883):
        self.dyson_ip = dyson_ip
        self.dyson_ssid = dyson_ssid
        self.dyson_password = dyson_password
        self.dyson_type = dyson_type
        self.port = port
        self.status_topic = f"{self.dyson_type}/{self.dyson_ssid}/status/current"
        self.command_topic = f"{self.dyson_type}/{self.dyson_ssid}/command"

    def hash_password(self):
        hash_obj = hashlib.sha512()
        hash_obj.update(self.dyson_password.encode('utf-8'))
        pwd_hash = base64.b64encode(hash_obj.digest()).decode('utf-8')
        return pwd_hash

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            bp.color("Successfully connected to your Dyson device", "green")
        elif rc == 4:
            bp.color(f"Failed to connect to your Dyson device. Code: {rc}", "red")
            os._exit(0)
        else: bp.color(f"Unknown status Code: {rc}", "red")

        client.subscribe(self.status_topic)

    @staticmethod
    def on_message(client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    @staticmethod
    def on_publish(client, userdata, mid):
        print(f"Message published with mid: {mid}")

    @staticmethod
    def get_rounded_timestamp():
        now = datetime.utcnow()

        rounded_now = now + timedelta(milliseconds=500)
        rounded_now = rounded_now - timedelta(milliseconds=rounded_now.microsecond // 1000 % 1000)

        rounded_timestamp = rounded_now.strftime('%Y-%m-%dT%H:%M:%S.') + f"{rounded_now.microsecond // 1000:03d}Z"

        return rounded_timestamp

    def send_command(self, speed, rotation, night_mod, fan_mod, client):
        now = self.get_rounded_timestamp()

        payload = {
            "msg": "STATE-SET",
            "time": now,
            "data": {
                "oson": rotation,
                "fnsp": speed,
                "nmod": night_mod,
                "fmod": fan_mod
            }
        }
        payload_str = json.dumps(payload)
        print(f"Publishing to topic {self.command_topic}: {payload_str}")
        result = client.publish(self.command_topic, payload_str)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish message. Return code: {result.rc}")

    @staticmethod
    def get_commands(speed, rotation, night_mod, fan_mod):
        if speed > 10:
            bp.color(f"Speed must be between 1 and 10", "red")
            os._exit(0)
        new_speed = f"000{str(speed)}" if len(f"000{str(speed)}") == 4 else f"00{str(speed)}"
        new_rotation = "ON" if rotation else "OFF"
        new_night_mod = "ON" if night_mod else "OFF"
        new_fan_mod = "FAN" if fan_mod else "OFF"
        return new_speed, new_rotation, new_night_mod, new_fan_mod

    def start(self, speed: int, rotation=False, night_mode=False, fan_mode=True):
        get_speed, get_rotation, get_night_mode, get_fan_mode = self.get_commands(speed, rotation, night_mode, fan_mode)
        client = mqtt.Client()
        password_hash = self.hash_password()
        client.username_pw_set(self.dyson_ssid, password_hash)

        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_publish = self.on_publish

        client.connect(self.dyson_ip, self.port, 60)
        client.loop_start()

        self.send_command(get_speed, get_rotation, get_night_mode, get_fan_mode, client)
        try:
            while True:
                pass

        except KeyboardInterrupt:
            client.loop_stop()
            client.disconnect()
            sys.exit()
