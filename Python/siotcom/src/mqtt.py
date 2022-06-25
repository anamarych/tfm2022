#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : mqtt.py
# @Author : a.cvillasenor@alumnos.upm.es
# Configuration of MQTT behaviour

# Local imports
from azureBase import AzureBase
from mongo import Mongo

# External imports
import paho.mqtt.client as mqtt

# Global Configuration
MQTT_HOST = "localhost" # este concentrador funciona como broker
MQTT_KEEPALIVE = 60
MQTT_PORT = 1883 # puerto default

class MQTT():
    def __init__(self, client_id, mongo: Mongo = None, az: AzureBase = None):
        self.mongo: Mongo = mongo
        self.az: AzureBase = az
        self.mqtt_client = mqtt.Client(client_id) #create client
        self.mqtt_client.on_connect = self.on_connect #on_connect callback
        self.mqtt_client.on_message = self.on_message #on_message callback
        self.mqtt_client.on_publish = self.on_publish #on_message callback

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        print("Connected to Mosquitto")
        
    def on_message(self, client: mqtt.Client, userdata, msg):
        if self.mongo is not None:
            self.mongo.save(msg.payload)
        else:
            self.az.send_data(msg.payload)            
    
    def on_publish(self, client:mqtt.Client, data, mid):
        print("Published", mid)

    def publish(self, topic, data):
        self.mqtt_client.publish(topic, data)
    
    def subscribe(self, topic, qos):
        self.mqtt_client.subscribe(topic, qos)
        print("Suscribed")
    
    def run(self):
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
