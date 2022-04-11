#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : prototipoLecturaTramas.py
# @Author : a.cvillasenor@alumnos.upm.es
# TODO: extrar Mqtt a la otra clase mqtt.py

import struct
import serial
import math
import datetime
import json

def main():
    #ejemplos de tramas obtenidas
    multi_buffer = [
        b'\x00\x02\x01\x05\x05\x01\xcd\xcc4A\x00\xcd\xcc\xb8A\x02\x00\xc0\x99C\np=\xb0A\x04\x10\xd7\xa5A\r\n',
        b'\x00\x02\x01\x05\x05\x01\xcd\xcc\x0cA\x00\x00\x00\xb8A\x02\x00@\xabC\n\xf0Q\xb6A\x0403\xa5A\r\n',
        b'\x00\x02\x01\x05\x05\x01\x00\x00\xb0@\x00\xcd\xcc\xb0A\x02\xff\xffVC\n',
        b'\x00\x02\x01\x06\x05\x01\x00\x00\xf4A\x0033\xb3A\x02\x00\x00\x00\x00\n@\xe1\xb0A\x04\xe0z\xa2A\r\n',
        b'\x00\x01\x01\x01\x05\x01\x9a\x99\xf9A\x00\xcd\xcc\xb0A\x02\x00\x00\x00\x00\n\xd0\xa3\xb2A\x04\xe0z\xa2A\r\n',
        b'\x00\x01\x01\x03\x05\x01\xcd\xcc\xe8A\x00\x00\x00\x98A\x02\x00\x00\x00\x00\n\xc0\xf5\x9eA\x04@\n\x8dA\r\n',
        b'\x00\x02\x01\x04\x05\x01\x00\x00\x08B\x00gf\x96A\x02\x00\x00\x00\x00\n\x80\xeb\x9bA\x04\xb0G\x87A\r\n',
        b'\x00\x01\x01\x07\x03\x01\xc0\x94\xdcA\x00\x1c\xb2\xcbA\x03\x00\x00\x00\x00\r\n'
        ]

    #cambiar buffer por la trama deseada para extraer la informacion
    buffer = b'\x00\x01\x01\x07\x03\x01\x80\x11\xf5A\x00\xec\xb4\xd3A\x03\x00\x00\x00\x00\r\n'
    print(buffer)
    f_data = format_sensor(buffer);
    print(f_data)

    
def format_sensor(data):
    now = datetime.datetime.now()
    mota = int.from_bytes(data[1:4], "big")
    x = {
        "id_concentrador": "000FF001",
        "time" : str(now.strftime('%Y%m%d_%H%M%S')),
        "id_mota": mota
        }
    
    total_sensores = data[4]  
    # la data de los sensores se presentan cada 5 bytes en la trama

    for i in range(5,len(data),5):
        if data[i] == 0:
            x["room_temp"] = "{:.2f}".format(struct.unpack('f', data[11:15])[0])
        elif data[i] == 1:
            x["humidity"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])
        elif data[i] == 2:
            x["luminosity"] = "{:.2f}".format(struct.unpack('f', data[16:20])[0])
        elif data[i] == 3:
            x["co2"] = struct.unpack('f', data[16:20])[0]
        elif data[i] == 4:
            x["surf_temp"] = "{:.2f}".format(struct.unpack('f', data[26:30])[0])
        elif data[i] == 5:
            x["abs_humidity"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])        
        elif data[i] == 7:
            x["movement"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])  
        elif data[i] == 10:
            x["add_temp"] = "{:.2f}".format(struct.unpack('f', data[21:25])[0])
        elif data[i] == 11:
            x["noise"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])
        data_json = json.dumps(x)
    return(data_json)

if __name__ == "__main__":
    main()