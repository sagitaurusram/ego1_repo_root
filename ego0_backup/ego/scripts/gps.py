import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)

port="/dev/ttyAMA0"
ser=serial.Serial(port,baudrate=9600,timeout=0.5)
data=''
try:
    while 1:
        try:
            data=ser.readline().decode()
            #print(data)
        except:
            print("bad")
        if '$GPGGA' in data:
            print(data)
            msg=pynmea2.parse(data)
            latval=msg.lat
            concatlat=""
            concatlat="Lat:"+str(latval)
            print(concatlat)
            longval=msg.lon
            concatlong=""
            concatlong="Long:"+str(longval)
            print(concatlong)
            time.sleep(1)
except KeyboardInterrupt:
    print("keyboard interrupt")