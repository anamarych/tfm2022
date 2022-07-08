#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : subMongo.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts as the MongoDB subscriber. Writes msgs to DB

#Local imports
from mongo import Mongo
from mqtt import MQTT

#External imports
from signal import pause
import sys

#Global Config
MQTT_CLIENT_ID = 'MONGO_CLIENT'
MQTT_TOPIC =("4405/000FF001/sensores/#")

def main():
    mongo = Mongo()
    mqtt = MQTT(MQTT_CLIENT_ID, mongo)
    mqtt.run()
    mongo.connect()
    mqtt.subscribe(MQTT_TOPIC)
    try:
        pause()
    except KeyboardInterrupt:
        mongo.disconnect()
        mqtt.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
