#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subMongo.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts only as a publisher

#Local imports
from mqtt import MQTT
from mongo import Mongo
from signal import pause
import sys

#External imports

#Global Config
MQTT_CLIENT_ID = 'MONGO_CLIENT'
MQTT_TOPIC =["4405/000FF001/sensores/#", "4007/000FF002/sensores/#"]

def main():
    mongo = Mongo()
    mqtt = MQTT(MQTT_CLIENT_ID, mongo)
    mongo.connect()
    mqtt.run()
    for t in MQTT_TOPIC:
        mqtt.subscribe(t, 2)
        
    try:
        pause()
    except KeyboardInterrupt:
        mongo.disconnect()
        mqtt.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
