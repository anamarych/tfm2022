#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : publisher.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts only as a publisher

#Local imports
from mqtt import MQTT
import json

#External imports
import struct
import serial
import math
import datetime
import sys

# Global Config
MQTT_TOPIC = "4405/000FF001/sensores" #formato {aula}/{concentrador}/sensores/{mota}
MQTT_CLIENT_ID = 'PUBLISH_CLIENT'
CLASS_ID = "4405"
HUB_ID = "000FF001"
EXPECTED_DATA_LENGTH = [12, 22, 32]

def main():
    mqtt = MQTT(MQTT_CLIENT_ID)
    mqtt.run()
    
    ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        )
    read_serial(ser, mqtt)
    
def read_serial(serial): 
    while 1:
        try:
            buffer = serial.read_until(expected=b'\r\n')
            if len(buffer) in EXPECTED_DATA_LENGTH:
                data, topic = format_sensor(buffer)
            else:
                data, topic = format_error(buffer)
            mqtt.publish(topic, data)
        except KeyboardInterrupt:
            mqtt.stop()
            sys.exit(0)
    
def format_error(data):
    now = datetime.datetime.now().isoformat()
    topic = MQTT_TOPIC + "/issue"
    document = {
        "time" : now,
        "class": CLASS_ID,
        "hub": HUB_ID,
        "node": "unknown",
        "data": {"error": data.decode("utf-8")}
        }
    data_json = json.dumps(document)    
    return(data_json, topic)

def format_sensor(data):
    now = datetime.datetime.now().isoformat()
    mota = str(int.from_bytes(data[1:4], "big"))
    topic = MQTT_TOPIC + "/" + mota
    document = {
        "time" : now,
        "class": CLASS_ID,
        "hub": HUB_ID,
        "node": mota
        }
    x = {}
    
    total_sensores = data[4]

    for i in range(5,len(data),5):
        if data[i] == 0:
            x["room_temp"] = float("{:-.2f}".format(struct.unpack('f', data[11:15])[0]))
        elif data[i] == 1:
            x["humidity"] = float("{:-.2f}".format(struct.unpack('f', data[6:10])[0]))
        elif data[i] == 2:
            x["luminosity"] = float("{:-.2f}".format(struct.unpack('f', data[16:20])[0]))
        elif data[i] == 3:
            x["co2"] = float("{:-.2f}".format(struct.unpack('f', data[16:20])[0]))
        elif data[i] == 4:
            x["surf_temp"] = float("{:-.2f}".format(struct.unpack('f', data[26:30])[0]))
        elif data[i] == 5:
            x["abs_humidity"] = float("{:-.2f}".format(struct.unpack('f', data[6:10])[0]))        
        elif data[i] == 7:
            x["movement"] = float("{:-.2f}".format(struct.unpack('f', data[6:10])[0]))  
        elif data[i] == 10:
            x["add_temp"] = float("{:-.2f}".format(struct.unpack('f', data[21:25])[0]))
        elif data[i] == 11:
            x["noise"] = float("{:-.2f}".format(struct.unpack('f', data[6:10])[0]))
        document["data"] = x
        data_json = json.dumps(document)    
    return(data_json, topic)

if __name__ == "__main__":
    main()
