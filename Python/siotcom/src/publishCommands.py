#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : publishCommands.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from the server and sends to Broker

#Local imports
from mqtt import MQTT

#External imports
import sys
import time

#Global Config
MQTT_CLIENT_ID = 'COMMAND_CLIENT'
MQTT_TOPIC =("4405/000FF001/actuadores/1")

def main():
    mqttc = MQTT(MQTT_CLIENT_ID)
    mqttc.run()
    time.sleep(3)
    try:
        data = "A sub should transform this into an actionable item"
        mqttc.publish(MQTT_TOPIC, data)
        print("publicado")
    except KeyboardInterrupt:
        mqttc.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
