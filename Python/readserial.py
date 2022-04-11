#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : readserial.py
# @Author : a.cvillasenor@alumnos.upm.es
# TODO: extrar Mqtt a la otra clase mqtt.py

import struct
import serial
import math
import datetime

def main():
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
        buffer = serial.read_until(expected=b'\r\n')
        print(buffer)
        f_data = format_sensor(buffer)
        print(f_data)
    
def format_sensor(data):
    now = datetime.datetime.now()
    mota = int.from_bytes(data[1:4], "big")
    x = {
        "id_concentrador": "000FF001", #se puede cambiar este ID para identificar a la raspberry
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
            x["co2"] = "{:.2f}".format(struct.unpack('f', data[16:20])[0])
        elif data[i] == 4:
            x["surf_temp"] = "{:.2f}".format(struct.unpack('f', data[26:30])[0])
        elif data[i] == 5:
            x["abs_humidity"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])        
        elif data[i] == 7:
            x["movement"] = struct.unpack('f', data[6:10])[0]
        elif data[i] == 10:
            x["add_temp"] = "{:.2f}".format(struct.unpack('f', data[21:25])[0])
        elif data[i] == 11:
            x["noise"] = "{:.2f}".format(struct.unpack('f', data[6:10])[0])           
    return(x)

if __name__ == "__main__":
    main()