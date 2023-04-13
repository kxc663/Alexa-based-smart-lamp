#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import sys
import time


PORT = 50001

configuration = {}
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("... connected")

    print("connection result: ")
    print(rc)


def on_disconnect(client, userdata, rc):
    print("... disconnected")


def go():
    i = 0
    while True:
        if i == sys.maxsize:
            i = 0

        message = json.dumps(configuration)
        print("message: " + message)
        configuration['value'] = i
        client.publish("devices/foobar/label/changed",
                       payload=json.dumps(configuration))
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    client.on_connect = on_connect
    print("... set connection listener")

    client.on_disconnect = on_disconnect
    print("... set disconnection listener")

    client.connect('localhost', port=PORT, keepalive=60)
    print("... tried to connect")

    client.loop_start()
    print("... starting client loop")

    go()
