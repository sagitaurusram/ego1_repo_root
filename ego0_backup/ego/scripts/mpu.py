import smbus
import time
 
import RPi.GPIO as gpio
import matplotlib.pyplot as plt
import numpy as np





 
 

 
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(25, gpio.OUT)
gpio.setup(8, gpio.OUT)
gpio.setup(7, gpio.OUT)
 
 

  
 
def cmd(ch):
  RS =18
  EN =23
  D4 =24
  D5 =25
  D6 =8
  D7 =7
  gpio.output(RS, 0)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  
def write(ch):
  RS =18
  EN =23
  D4 =24
  D5 =25
  D6 =8
  D7 =7
  gpio.output(RS, 1)
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x10==0x10:
    gpio.output(D4, 1)
  if ch&0x20==0x20:
    gpio.output(D5, 1)
  if ch&0x40==0x40:
    gpio.output(D6, 1)
  if ch&0x80==0x80:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)
  # Low bits
  gpio.output(D4, 0)
  gpio.output(D5, 0)
  gpio.output(D6, 0)
  gpio.output(D7, 0)
  if ch&0x01==0x01:
    gpio.output(D4, 1)
  if ch&0x02==0x02:
    gpio.output(D5, 1)
  if ch&0x04==0x04:
    gpio.output(D6, 1)
  if ch&0x08==0x08:
    gpio.output(D7, 1)
  gpio.output(EN, 1)
  time.sleep(0.005)
  gpio.output(EN, 0)

 
 
def readMPU(bus,addr):
    high = bus.read_byte_data(0x68, addr)
    low = bus.read_byte_data(0x68, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def accel(bus,AxCal,AyCal):
    x = readMPU(bus,0x3B)
    y = readMPU(bus,0x3D)
    z = readMPU(bus,0x3F)
    Ax = (x/16384.0-AxCal) 
    Ay = (y/16384.0-AyCal) 
    #Az = (z/16384.0-AzCal)
    #print("Ax:"+str(Ax))
    #print("Ay:"+str(Ay))
    return [Ax,Ay]
    
    #print("Az:"+str(Az))
    #time.sleep(.01)
 
 
def temp():
  tempRow=readMPU(TEMP)
  tempC=(tempRow / 340.0) + 36.53
  tempC="%.2f" %tempC
  print(tempC)
  print("Temp: ")
  print(str(tempC))
  time.sleep(.2)
 
    
    

def iMPU():
    #begin();
    print("iMPU")
    PWR_M   = 0x6B
    DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_EN   = 0x38
    ACCEL_X = 0x3B
    ACCEL_Y = 0x3D
    ACCEL_Z = 0x3F
    TEMP = 0x41
    bus = smbus.SMBus(1)
    Device_Address = 0x68   # device address
     
    AxCal=0
    AyCal=0
    AzCal=0
    cmd(0x33) 
    cmd(0x32) 
    cmd(0x06)
    cmd(0x0C) 
    cmd(0x28) 
    cmd(0x01) 
    time.sleep(0.0005)
    print("MPU6050 Interface")
    time.sleep(2)
    #InitMPU()
    bus.write_byte_data(Device_Address, DIV, 7)#sample rate reigster
    bus.write_byte_data(Device_Address, PWR_M, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_EN, 1)
    time.sleep(1)
    #calibrate()
    x=0
    y=0
    z=0
    for i in range(50):
      x = x + readMPU(bus,ACCEL_X)
      y = y + readMPU(bus,ACCEL_Y)
      z = z + readMPU(bus,ACCEL_Z)
    x= x/50
    y= y/50
    z= z/50
    AxCal = x/16384.0
    AyCal = y/16384.0
    AzCal = z/16384.0
    print(AxCal)
    print(AyCal)
    print(AzCal)
    i=0
    td=0
    print(bus,AxCal,AyCal)
    return bus,AxCal,AyCal

def rMPU(bus,AxCal,AyCal,duration,ts):
    print("rMPU")
    path_a={}
    i=0
    td=0
    for k in range(1):
        print("Stat and collAccel")
        time.sleep(1)
        start_time=time.time();
        while td<=duration:
        #while 1:
            path_a[i]=accel(bus,AxCal,AyCal)
            #print(path_a[i])
            time.sleep(ts)
            td=td+ts
            i=i+1
        end_time=time.time();
    print("MPU  :"+str(end_time-start_time))
    #print(path_a)
    l=len(path_a)
    print("in plot data function")
    ux_1=0
    uy_1=0
    dt=ts
    sx_total=0
    sy_total=0
    for i in range(l):
        ax_1=path_a[i][0]
        ay_1=path_a[i][1]
        ux_2=ux_1+(ax_1*dt)
        uy_2=uy_1+(ay_1*dt)
        sx_2=ux_1*dt + ax_1*dt*dt*0.5
        sy_2=uy_1*dt + ay_1*dt*dt*0.5
        sx_total=sx_total+sx_2
        sy_total=sy_total+sy_2
        ux_1=ux_2
        uy_1=uy_2
        path_a[i].append(sx_2)
        path_a[i].append(sy_2)
        path_a[i].append(sx_total)
        path_a[i].append(sy_total)
    print("format is ")
    print("x_acc,  y_acc, x_dis_incr,y_dis_incr,xtot,ytot")
    for keys in path_a.keys():
        print(str(keys)+' : '+str(path_a[keys][0:2]))
    #return acc_a
    l=len(path_a)
    print(str(l))
    t=np.linspace(0,l,l)
    x_dis=[]
    y_dis=[]
    for i in range(l):
      x_dis.append(path_a[i][4])
      y_dis.append(path_a[i][5])
    plt.plot(t,y_dis,label='acc dis')
    plt.plot(t,x_dis,label='y dis')
    plt.legend()
    plt.show()
    plt.scatter(x_dis,y_dis)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()



'''    
def runAndPlotMPU():
    mpu_path={}
    iMPU()
    temp()
    mpu_path=runMPU(mpu_path,5)
    mpu_path=plotData(mpu_path,0.1)
    plotMPU(mpu_path)
'''
en=0
if(en):
    bus,xCal,yCal=iMPU()
    rMPU(bus,xCal,yCal,6,0.1)