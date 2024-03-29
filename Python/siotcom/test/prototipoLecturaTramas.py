#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : prototipoLecturaTramas.py
# @Author : a.cvillasenor@alumnos.upm.es

import struct
import math
import datetime
import json
import sys
import os

myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path

path = Path(myDir)
a=str(path.parent.absolute())

sys.path.append(a)

from mqtt import MQTT # puede dar error dependiendo de la estructura del proyecto

CLASS_ID = "4407"
HUB_ID = "000FF002"
EXPECTED_DATA_LENGTH = [10, 20, 30]
MQTT_CLIENT_ID = 'PUBLISH_CLIENT2'
MQTT_TOPIC = "4007/000FF002/sensores" #formato {aula}/{concentrador}/sensores/{mota}

def main():
    mqtt = MQTT(MQTT_CLIENT_ID)
    mqtt.run()

    #ejemplos de tramas obtenidas
    multi_buffer = [
        b'[BH1750] Device is not configured!', #Error #34
        b'\x00\x02\x01\x05\x05\x01\xcd\xcc4A\x00\xcd\xcc\xb8A\x02\x00\xc0\x99C\np=\xb0A\x04\x10\xd7\xa5A', #30
        b'\x00\x02\x01\x05\x05\x01\xcd\xcc\x0cA\x00\x00\x00\xb8A\x02\x00@\xabC\n\xf0Q\xb6A\x0403\xa5A', #30
        b'\x00\x02\x01\x05\x05\x01\x00\x00\xb0@\x00\xcd\xcc\xb0A\x02\xff\xffVC\n', #Error #21
        b'\x00\x02\x01\x06\x05\x01\x00\x00\xf4A\x0033\xb3A\x02\x00\x00\x00\x00\n@\xe1\xb0A\x04\xe0z\xa2A', #30
        b'\x00\x01\x01\x01\x05\x01\x9a\x99\xf9A\x00\xcd\xcc\xb0A\x02\x00\x00\x00\x00\n\xd0\xa3\xb2A\x04\xe0z\xa2A', #30
        b'\x00\x01\x01\x03\x05\x01\xcd\xcc\xe8A\x00\x00\x00\x98A\x02\x00\x00\x00\x00\n\xc0\xf5\x9eA\x04@\n\x8dA', #30
        b'\x00\x02\x01\x04\x05\x01\x00\x00\x08B\x00gf\x96A\x02\x00\x00\x00\x00\n\x80\xeb\x9bA\x04\xb0G\x87A', #30
        b'\x00\x01\x01\x07\x03\x01\xc0\x94\xdcA\x00\x1c\xb2\xcbA\x03\x00\x00\x00\x00', #20 co2
        b'\x00\x02\x01\x05\x01\x07\x00\x00\x00\x01', #10 movimiento
        b'\x00\x01\x01\x07\x01\x0b\x00\x000A' #10 noise
        ]

    #cambiar buffer por la trama deseada para extraer la informacion
    buffer = multi_buffer[1]
    print(buffer)
    if len(buffer) in EXPECTED_DATA_LENGTH:
        data, topic = format_sensor(buffer)
    else:
        data, topic = format_error(buffer)
    print(data)
    mqtt.publish(topic, data)

def format_error(data):
    now = datetime.datetime.now().isoformat() #MongoDB format
    document = {
        "time" : now,
        "class": CLASS_ID,
        "hub": HUB_ID,
        "node": "unknown",
        "data": {"error": data.decode('utf-8')}
        }
    return document

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

    # la data de los sensores se presentan cada 5 bytes en la trama
    for i in range(5,len(data),5):
        if data[i] == 0:
            x["room_temp"] = float("{:.2f}".format(struct.unpack('f', data[11:15])[0]))
        elif data[i] == 1:
            x["humidity"] = float("{:.2f}".format(struct.unpack('f', data[6:10])[0]))
        elif data[i] == 2:
            x["luminosity"] = float("{:.2f}".format(struct.unpack('f', data[16:20])[0]))
        elif data[i] == 3:
            x["co2"] = struct.unpack('f', data[16:20])[0]
        elif data[i] == 4:
            x["surf_temp"] = float("{:.2f}".format(struct.unpack('f', data[26:30])[0]))
        elif data[i] == 5:
            x["abs_humidity"] = float("{:.2f}".format(struct.unpack('f', data[6:10])[0]))        
        elif data[i] == 7:
            x["movement"] = float("{:.2f}".format(struct.unpack('f', data[6:10])[0]))  
        elif data[i] == 10:
            x["add_temp"] = float("{:.2f}".format(struct.unpack('f', data[21:25])[0]))
        elif data[i] == 11:
            x["noise"] = float("{:.2f}".format(struct.unpack('f', data[6:10])[0]))
        document["data"] = x
        data_json = json.dumps(document)    
    return(data_json,topic)

if __name__ == "__main__":
    main()