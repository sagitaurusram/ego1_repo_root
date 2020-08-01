import serial
import time
ser1=serial.Serial('/dev/ttyUSB0',38400)
print(ser1.name)
time.sleep(1)
ser1.write('GET Kpr\n'.encode())
time.sleep(1)
while 1:
    ser1.write('M2 F 3000\n'.encode())
    #time.sleep(5)
    #time.sleep(0.5)
    line=' '
    while 'Ok' not in str(line):
        line=ser1.readline()
        print(line)
    ser1.write('SET Kpr 0.2\n'.encode())
    while 'Ok' not in str(line):
        line=ser1.readline()
        print(line)
    ser1.write('M2 R 5000\n'.encode())
    line=''
    while 'Ok' not in str(line):
        line=ser1.readline()
        print(line)
#print('response '+line.decode('ascii'))
#ser1.write('M1 F 1000\n'.encode())
#ser1.write('GET counterL\n'.encode())

        #time.sleep(1)
time.sleep(2)
