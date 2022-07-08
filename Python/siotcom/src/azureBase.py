#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : azureBase.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and connects to Azure IoTHub by using the env variable IOTHUB_DEVICE_CONNECTION_STRING

# Local imports

# External imports
import json
import logging
import os

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from datetime import timedelta, datetime

#Global Config
logging.basicConfig(level=logging.ERROR)

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
#model_id = "dtmi:com:example:siotcom;1"

class AzureBase():
    def __init__(self):
        self.client = None
            
    def connect(self):
        # Connect the client
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING) #product_info=model_id)
        self.client.connect()
        print("Connected to IoTHub")
    
    def disconnect(self):
        self.client.shutdown()
        print("Disconnected from IoTHub")
        
    def send_data(self, data):
        msg = Message(data)
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        print("Message sent to IoTHub")
        self.client.send_message(msg)
        