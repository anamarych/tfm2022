#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : publisher.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and acts only as a publisher

#Local imports
from mqtt import MQTT

#External imports
import struct
import serial
import math
import datetime
import sys

#Global Config
MQTT_CLIENT_ID = 'PUBLISH_CLIENT'
CLASS_ID = "4405"
HUB_ID = "000FF001"

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
    read_serial(ser)
    
def read_serial(serial): 
    while 1:
        try:
            buffer = serial.read_until(expected=b'\r\n')
            f_data = format_sensor(buffer)
            mqtt.do_publish(f_data)
        except KeyboardInterrupt:
            mqtt.stop()
            sys.exit(0)
    
def format_sensor(data):
    now = datetime.datetime.now().isoformat() #MongoDB format
    mota = str(int.from_bytes(data[1:4], "big"))
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
        elif data[i] == 10: #documentation is marked as 9, arduino sends by 10
            x["add_temp"] = float("{:.2f}".format(struct.unpack('f', data[21:25])[0]))
        elif data[i] == 11:
            x["noise"] = float("{:.2f}".format(struct.unpack('f', data[6:10])[0]))
        document["data"] = x
        data_json = json.dumps(document)    
    return(data_json)

if __name__ == "__main__":
    main()