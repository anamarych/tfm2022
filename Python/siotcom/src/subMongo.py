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
#Global Config
MQTT_CLIENT_ID = 'MONGO_CLIENT'
MQTT_TOPIC =("4405/000FF001/sensores/#")

def main():
    try:
        mongo = Mongo()
        mqtt = MQTT(MQTT_CLIENT_ID, mongo)
        mongo.connect()
        mqtt.run()
        mqtt.subscribe(MQTT_TOPIC)
    except KeyboardInterrupt:
        mqtt.stop()
        mongo.disconnect()

if __name__ == "__main__":
    main()
