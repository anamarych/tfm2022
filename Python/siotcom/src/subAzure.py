#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subAzure.py
# @Author : a.cvillasenor@alumnos.upm.es
# This is the subscriber for Azure IoTHub

#Local imports
from azureBase import AzureBase
from mqtt import MQTT

#External imports
from singal import pause
import sys

#Global Config
MQTT_CLIENT_ID = 'AZURE_CLIENT'
MQTT_TOPIC =("4405/000FF001/sensores/#")

def main():
    az = AzureBase()
    mqtt = MQTT(MQTT_CLIENT_ID, None, az)
    az.connect()
    mqtt.run()
    mqtt.subscribe(MQTT_TOPIC, 2)
    try:
        pause()
    except KeyboardInterrupt:
        az.disconnect()
        mqtt.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
