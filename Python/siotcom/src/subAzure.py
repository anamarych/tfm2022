#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subAzure.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts as the Azure subscriber. Writes msgs to Azure IOTHUB

#Local imports
from mqtt import MQTT

#External imports

#Global Config
MQTT_CLIENT_ID = 'AZURE_CLIENT'
CLASS_ID = "4405"
HUB_ID = "000FF001"
MQTT_TOPIC =("4405/000FF001/sensores/#")

def main():
    try:
        mqtt = MQTT(MQTT_CLIENT_ID)
        mqtt.run()
        mqtt.subscribe(MQTT_TOPIC)
    except KeyboardInterrupt:
        mqtt.stop()

if __name__ == "__main__":
    main()
