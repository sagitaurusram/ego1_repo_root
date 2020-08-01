import serial
import time
from threading import Thread


ser1=serial.Serial('/dev/ttyUSB0',38400)
data=''
def sendAndWaitForResponse(cmd,resp):
    result=-1
    ser1.write(cmd.encode())
    time.sleep(1)
    while resp not in  str(data):
        time.sleep(1)
        print('waiting for response')
    print('response received')
    if(resp=='-'):
        x=str(data)
        print(x)
        part1=x[x.find('-'):]
        part2=part1[1:part1.find('\\')]
        print(int(part2))
        time.sleep(1)
        result=int(part2)
    return result
def read(ser):
    global data
    while 1:
        try:
            data=ser.read(ser.in_waiting or 1)
            if data:
                print(data)
        except serial.SerialException:
            print('error')




print(ser1.name)
print(ser1.name)
time.sleep(1)
ser1.write('GET Kpr\n'.encode())
time.sleep(1)

process=Thread(target=read,args=[ser1])
process.start()
time.sleep(1)

sendAndWaitForResponse('SET Kpr 0.0\n','OK')
sendAndWaitForResponse('M1 F 1000\n','Ended')
sendAndWaitForResponse('GET counterL\n','-')
sendAndWaitForResponse('GET counterR\n','-')
 

process.join()
