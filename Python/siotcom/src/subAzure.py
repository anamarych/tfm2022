#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subAzure.py
# @Author : a.cvillasenor@alumnos.upm.es
# This is the subscriber for Azure IoTHub

#Local imports
from azureBase import AzureBase
from mqtt import MQTT

#Global Config
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
MQTT_CLIENT_ID = 'AZURE_CLIENT'
MQTT_TOPIC =("4405/000FF001/sensores/#")
logging.basicConfig(level=logging.ERROR)

def main():
    az = AzureBase()
    mqtt = MQTT(MQTT_CLIENT_ID, None, az)
    az.connect()
    mqtt.run()
    mqtt.subscribe(MQTT_TOPIC, 2)

if __name__ == "__main__":
    main()
