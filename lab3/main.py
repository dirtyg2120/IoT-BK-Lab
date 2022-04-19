print("IoT Gateway")
import paho.mqtt.client as mqttclient
import time
import json
import serial.tools.list_ports

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
mess = ""

#TODO: Add your token and your comport
#Please check the comport in the device manager
THINGS_BOARD_ACCESS_TOKEN = "fmdwvzxv1BgEY6uGa8zr"
bbc_port = "COM4"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    #TODO: Add your source code to publish data to the server
    collect_data = {
        splitData[1]: splitData[2],
    }

    client.publish("v1/devices/me/telemetry", json.dumps(collect_data), 1)

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")

def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data_led = {'value': True}
    temp_data_fan = {'value': True}
    cmd = -1
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLed":
            temp_data_led['value'] = jsonobj['params']
            if temp_data_led['value'] is True:
                cmd = 0
            else:
                cmd = 1
            client.publish('v1/devices/me/attributes', json.dumps(temp_data_led), 1)
        if jsonobj['method'] == "setFan":
            temp_data_fan['value'] = jsonobj['params']
            if temp_data_fan['value'] is True:
                cmd = 2
            else:
                cmd = 3
            client.publish('v1/devices/me/attributes', json.dumps(temp_data_fan), 1)
    except:
        pass

    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())

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


while True:

    if len(bbc_port) >  0:
        readSerial()

    time.sleep(1)