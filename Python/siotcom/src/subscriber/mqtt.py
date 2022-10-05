#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : mqtt.py
# @Author : a.cvillasenor@alumnos.upm.es
# Configuration of MQTT behaviour

# Local imports

# External imports
import paho.mqtt.client as mqtt

# Global Configuration
MQTT_HOST = "#.#.#.#" # este concentrador no funciona como broker. debe tener como host la ip del broker
MQTT_KEEPALIVE = 60
MQTT_PORT = 1883 # puerto default

class MQTT():
    def __init__(self, client_id):
        self.mqtt_client = mqtt.Client(client_id) #create client
        self.mqtt_client.on_connect = self.on_connect #on_connect callback
        self.mqtt_client.on_publish = self.on_publish #on_publish callback
        self.mqtt_client.on_disconnect = self.on_disconnect #on_disconnect callback

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Mosquitto")
        else:
            print("Failed to connect to Mosqutito")
    
    def on_disconnect(self, client:mqtt.Client, userdata, rc=0):
        print("Disconnected from Mosquitto")
                    
    def on_publish(self, client:mqtt.Client, data, mid):
        print("Published", mid)

    def publish(self, topic, data):
        self.mqtt_client.publish(topic, data)
    
    def subscribe(self, topic, qos):
        self.mqtt_client.subscribe(topic, qos)
        print("Suscribed to ", topic)
    
    def run(self):
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
