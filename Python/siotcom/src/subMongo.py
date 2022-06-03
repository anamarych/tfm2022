#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subscriber.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts only as a publisher

#Local imports
from mqtt import MQTT

#External imports


#Global Config
MQTT_CLIENT_ID = 'MONGO_CLIENT'
CLASS_ID = "4405"
HUB_ID = "000FF001"
MQTT_TOPIC =("4405/000FF001/sensores")

def main():
    mqtt = MQTT(MQTT_CLIENT_ID)
    mqtt.run()
    mqtt.subscribe(MQTT_TOPIC)

if __name__ == "__main__":
    main()
