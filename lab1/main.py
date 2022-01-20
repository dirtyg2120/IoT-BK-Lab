print("Hello ThingsBoard!")
import requests
import paho.mqtt.client as mqttclient
import time
import json
from random import randrange
from dotenv import load_dotenv
import os

load_dotenv()

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {"value": True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj["method"] == "setValue":
            temp_data["value"] = jsonobj["params"]
            client.publish("v1/devices/me/attributes", json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

LATITUDE = 10.8231
LONGITUDE = 106.6297

counter = 0
while True:
    temp = randrange(100)
    humi = randrange(100)
    light_intesity = randrange(100)
    try:
        response = requests.get(f"https://ipinfo.io/json").json()
        lat, lon = response["loc"].split(",")
    except:
        lat, lon = LATITUDE, LONGITUDE

    collect_data = {
        "temperature": temp,
        "humidity": humi,
        "light": light_intesity,
        "latitude": lat,
        "longitude": lon,
    }

    client.publish("v1/devices/me/telemetry", json.dumps(collect_data), 1)
    time.sleep(10)
