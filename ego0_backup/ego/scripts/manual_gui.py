import tkinter as tk
from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
import serial
import io
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import smbus
import time
'''
MPU settings
'''

PWR_M   = 0x6B
DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47
TEMP = 0x41
bus = smbus.SMBus(1)
Device_Address = 0x68   # device address
 
AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0
 
 
RS =18
EN =23
D4 =24
D5 =25
D6 =8
D7 =7
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(D4, GPIO.OUT)
GPIO.setup(D5, GPIO.OUT)
GPIO.setup(D6, GPIO.OUT)
GPIO.setup(D7, GPIO.OUT)

def begin():
  cmd(0x33) 
  cmd(0x32) 
  cmd(0x06)
  cmd(0x0C) 
  cmd(0x28) 
  cmd(0x01) 
  time.sleep(0.0005)
 
def cmd(ch): 
  GPIO.output(RS, 0)
  GPIO.output(D4, 0)
  GPIO.output(D5, 0)
  GPIO.output(D6, 0)
  GPIO.output(D7, 0)
  if ch&0x10==0x10:
    GPIO.output(D4, 1)
  if ch&0x20==0x20:
    GPIO.output(D5, 1)
  if ch&0x40==0x40:
    GPIO.output(D6, 1)
  if ch&0x80==0x80:
    GPIO.output(D7, 1)
  GPIO.output(EN, 1)
  time.sleep(0.005)
  GPIO.output(EN, 0)
  # Low bits
  GPIO.output(D4, 0)
  GPIO.output(D5, 0)
  GPIO.output(D6, 0)
  GPIO.output(D7, 0)
  if ch&0x01==0x01:
    GPIO.output(D4, 1)
  if ch&0x02==0x02:
    GPIO.output(D5, 1)
  if ch&0x04==0x04:
    GPIO.output(D6, 1)
  if ch&0x08==0x08:
    GPIO.output(D7, 1)
  GPIO.output(EN, 1)
  time.sleep(0.005)
  GPIO.output(EN, 0)
  
def write(ch): 
  GPIO.output(RS, 1)
  GPIO.output(D4, 0)
  GPIO.output(D5, 0)
  GPIO.output(D6, 0)
  GPIO.output(D7, 0)
  if ch&0x10==0x10:
    GPIO.output(D4, 1)
  if ch&0x20==0x20:
    GPIO.output(D5, 1)
  if ch&0x40==0x40:
    GPIO.output(D6, 1)
  if ch&0x80==0x80:
    GPIO.output(D7, 1)
  GPIO.output(EN, 1)
  time.sleep(0.005)
  GPIO.output(EN, 0)
  # Low bits
  GPIO.output(D4, 0)
  GPIO.output(D5, 0)
  GPIO.output(D6, 0)
  GPIO.output(D7, 0)
  if ch&0x01==0x01:
    GPIO.output(D4, 1)
  if ch&0x02==0x02:
    GPIO.output(D5, 1)
  if ch&0x04==0x04:
    GPIO.output(D6, 1)
  if ch&0x08==0x08:
    GPIO.output(D7, 1)
  GPIO.output(EN, 1)
  time.sleep(0.005)
  GPIO.output(EN, 0)
def clear():
  cmd(0x01)
 
def Print(Str):
  l=0;
  l=len(Str)
  for i in range(l):
    write(ord(Str[i]))
    
def setCursor(x,y):
        if y == 0:
                n=128+x
        elif y == 1:
                n=192+x
        cmd(n)
 
 
def InitMPU():
    bus.write_byte_data(Device_Address, DIV, 7)#sample rate reigster
    bus.write_byte_data(Device_Address, PWR_M, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_EN, 1)
    time.sleep(1)
 
def display(x,y,z):
      x=x*100
      y=y*100
      z=z*100
      x= "%d" %x
      y= "%d" %y
      z= "%d" %z
      print("X     Y     Z")
      print(str(x))
      print("   ")
      print(str(y))
      print("   ")
      print(str(z))
      print("   ")
      print(x)
      print(y)
      print(z)
 
 
def readMPU(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def accel():
    x = readMPU(ACCEL_X)
    y = readMPU(ACCEL_Y)
    z = readMPU(ACCEL_Z)
    Ax = (x/16384.0-AxCal) 
    Ay = (y/16384.0-AyCal) 
    #Az = (z/16384.0-AzCal)
    #print("Ax:"+str(Ax))
    #print("Ay:"+str(Ay))
    return [Ax,Ay]
    
    #print("Az:"+str(Az))
    #time.sleep(.01)
 
def gyro():
      global GxCal
      global GyCal
      global GzCal
      x = readMPU(GYRO_X)
      y = readMPU(GYRO_Y)
      z = readMPU(GYRO_Z)
      Gx = x/131.0 - GxCal
      Gy = y/131.0 - GyCal
      Gz = z/131.0 - GzCal
      #print "X="+str(Gx)
      display(Gx,Gy,Gz)
      #time.sleep(.01)
 
def temp():
  tempRow=readMPU(TEMP)
  tempC=(tempRow / 340.0) + 36.53
  tempC="%.2f" %tempC
  print(tempC)
  print("Temp: ")
  print(str(tempC))
  time.sleep(.2)
 
def calibrate():
  clear()
  Print("Calibrate....")
  global AxCal
  global AyCal
  global AzCal
  x=0
  y=0
  z=0
  for i in range(50):
      x = x + readMPU(ACCEL_X)
      y = y + readMPU(ACCEL_Y)
      z = z + readMPU(ACCEL_Z)
  x= x/50
  y= y/50
  z= z/50
  AxCal = x/16384.0
  AyCal = y/16384.0
  AzCal = z/16384.0
  print(AxCal)
  print(AyCal)
  print(AzCal)
  global GxCal
  global GyCal
  global GzCal
  x=0
  y=0
  z=0
  for i in range(50):
    x = x + readMPU(GYRO_X)
    y = y + readMPU(GYRO_Y)
    z = z + readMPU(GYRO_Z)
  x= x/50
  y= y/50
  z= z/50
  GxCal = x/131.0
  GyCal = y/131.0
  GzCal = z/131.0
  print(GxCal)
  print(GyCal)
  print(GzCal)

def plotMPU(path):
    #print(path)
    l=len(path)
    print(str(l))
    t=np.linspace(0,l,l)
    x_dis=[]
    y_dis=[]
    for i in range(l):
      x_dis.append(path[i][4])
      y_dis.append(path[i][5])
    plt.plot(t,y_dis,label='acc dis')
    plt.legend()
    plt.show()
    
def plotData(acc_a,ts):
    l=len(acc_a)
    print("in plot data function")
    clear()
    ux_1=0
    uy_1=0
    dt=ts
    sx_total=0
    sy_total=0
    for i in range(l):
        ax_1=acc_a[i][0]
        ay_1=acc_a[i][1]
        ux_2=ux_1+(ax_1*dt)
        uy_2=uy_1+(ay_1*dt)
        sx_2=ux_1*dt + ax_1*dt*dt*0.5
        sy_2=uy_1*dt + ay_1*dt*dt*0.5
        sx_total=sx_total+sx_2
        sy_total=sy_total+sy_2
        ux_1=ux_2
        uy_1=uy_2
        acc_a[i].append(sx_2)
        acc_a[i].append(sy_2)
        acc_a[i].append(sx_total)
        acc_a[i].append(sy_total)
    print("format is ")
    print("x_acc,  y_acc, x_dis_incr,y_dis_incr,xtot,ytot")
    for keys in acc_a.keys():
        print(str(keys)+' : '+str(acc_a[keys]))
    return acc_a
    

def iMPU():
    begin();
    print("MPU6050 Interface")
    time.sleep(2)
    InitMPU()
    calibrate()
    
def runMPU(path_a,duration):
    i=0
    td=0
    for k in range(1):
      print("Stat and collAccel")
      time.sleep(1)
      start_time=time.time();
      while td<=duration:
      #while 1:
        path_a[i]=accel()
        print(accel())
        time.sleep(0.1)
        td=td+0.1
        i=i+1
      end_time=time.time();
      print("MPU  :"+str(end_time-start_time))
      #print(path_a)
      return path_a
'''
end of MPU
'''
en=0
if(en):
    mpu_path={}
    iMPU()
    temp()
    mpu_path=runMPU(mpu_path,5)
    mpu_path=plotData(mpu_path,0.1)
    plotMPU(mpu_path)
    exit()
threads=[]


accPlotEn=1
win=tk.Tk()
win.title("EGO gui")


plot_win=tk.Tk()
plot_win.title("Sensor plots")
'''
fig=plt.figure()
ax=fig.gca(projection='3d')
x=np.arange(-5,5,0.25)
y=np.arange(-5,5,0.25)
x,y=np.meshgrid(x,y)
r=np.sqrt(x**2+y**2)
z=np.sin(r)
surf=ax.plot_surface(x,y,z,rstride=1,cstride=1,cmap=cm.coolwarm,linewidth=0,antialiased=False)
ax.set_zlim(-1.01,1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf,shrink=0.5,aspect=5)
plt.show()
'''
auto=1
SERIAL_EN=0
if SERIAL_EN:
    ser1=serial.Serial('/dev/ttyUSB0',38400)
    print(ser1.name)
    line=ser1.readline()
    print(line)

mpuPath={}
  
vleft_turn=0
vright_turn=0
vleft_fwd=0
vright_fwd=0

#waypoints
tmap_wp=[]
for i in range(10):
    tmap_wp.append((0,0,0))
ltmap_wp1_name=tk.StringVar(value=90)
ltmap_wp2_name=tk.StringVar(value=0)
ltmap_wp3_name=tk.StringVar(value=90)
ltmap_wp4_name=tk.StringVar(value=90)
ltmap_wp5_name=tk.StringVar(value=90)
ltmap_wp6_name=tk.StringVar(value=0)
ltmap_wp7_name=tk.StringVar(value=0)
ltmap_wp8_name=tk.StringVar(value=0)
ltmap_wp9_name=tk.StringVar(value=0)
ltmap_wp10_name=tk.StringVar(value=0)

rtmap_wp1_name=tk.StringVar(value=90)
rtmap_wp2_name=tk.StringVar(value=90)
rtmap_wp3_name=tk.StringVar(value=90)
rtmap_wp4_name=tk.StringVar(value=0)
rtmap_wp5_name=tk.StringVar(value=90)
rtmap_wp6_name=tk.StringVar(value=0)
rtmap_wp7_name=tk.StringVar(value=0)
rtmap_wp8_name=tk.StringVar(value=0)
rtmap_wp9_name=tk.StringVar(value=0)
rtmap_wp10_name=tk.StringVar(value=0)

tmap_t1_name=tk.StringVar(value=5)
tmap_t2_name=tk.StringVar(value=2)
tmap_t3_name=tk.StringVar(value=4)
tmap_t4_name=tk.StringVar(value=2)
tmap_t5_name=tk.StringVar(value=5)
tmap_t6_name=tk.StringVar(value=0)
tmap_t7_name=tk.StringVar(value=0)
tmap_t8_name=tk.StringVar(value=0)
tmap_t9_name=tk.StringVar(value=0)
tmap_t10_name=tk.StringVar(value=0)

icr1=tk.StringVar(value=0)
icr2=tk.StringVar(value=0)
icr3=tk.StringVar(value=0)
icr4=tk.StringVar(value=0)
icr5=tk.StringVar(value=0)
icr6=tk.StringVar(value=0)
icr7=tk.StringVar(value=0)
icr8=tk.StringVar(value=0)
icr9=tk.StringVar(value=0)
icr10=tk.StringVar(value=0)

dis1=tk.StringVar(value=1)
dis2=tk.StringVar(value=1)
dis3=tk.StringVar(value=1)
dis4=tk.StringVar(value=1)
dis5=tk.StringVar(value=1)
dis6=tk.StringVar(value=1)
dis7=tk.StringVar(value=1)
dis8=tk.StringVar(value=1)
dis9=tk.StringVar(value=1)
dis10=tk.StringVar(value=1)

print(GPIO.RPI_INFO)
GPIO.setmode(GPIO.BCM)
arduinoHwrstPin=2
GPIO.setup(arduinoHwrstPin,GPIO.OUT,initial=1)

def sendSerCmd(cmd):
    if SERIAL_EN:
        print(cmd)
        ser1.write(cmd.encode())
        time.sleep(1)
        ser1.write('v=l0r0z/r/n'.encode())
def leftAction():
    global vright_turn
    print("left clicked")
    sendSerCmd('v=l0'+'r'+str(vright_turn)+'z/r/n')
    
def rightAction():
    global vleft_turn
    print("right clicked")
    sendSerCmd('v=l'+str(vleft_turn)+'r0z/r/n')
    
def frontAction():
    global vleft_fwd
    global vright_fwd
    print("front clicked")
    print(vleft_fwd)
    #sendSerCmd('v=l'+str(vleft_fwd)+'r'+str(vright_fwd)+'z/r/n')
    sendSErCmd
def stopAction():
    print("stop clicked")
    sendSerCmd('v=l0r0z/r/n')
def hwrstAction():
    print("Hard Reset clicked")
    GPIO.output(arduinoHwrstPin,GPIO.LOW)
    time.sleep(1)
    GPIO.output(arduinoHwrstPin,GPIO.HIGH)
    print("Hard Reset released")
  
def swrstAction():
    print("Soft Reset clicked")

def velUpdateAction():
    global vleft_turn
    global vright_turn
    global vleft_fwd
    global vright_fwd
    print("Updating velocity")
    vleft_turn=vleft_turn_name.get()
    print(vleft_turn)
    vright_turn=vright_turn_name.get()
    print(vright_turn)
    vleft_fwd=vfront_name.get()
    print(vleft_fwd)
    vright_fwd=rfront_name.get()
    print(vright_fwd)
def leftSldAction(event):
    global vleft_turn
    #print("Updating velocity via Slider")
    vleft_turn=int(vleft_turn_slider.get())
    vleft_turn_name_Entered.delete(0,tk.END)
    vleft_turn_name_Entered.insert(0,vleft_turn)
    print(vleft_turn)
def rightSldAction(event):
    global vright_turn   
    vright_turn=int(vright_turn_slider.get())
    vright_turn_name_Entered.delete(0,tk.END)
    vright_turn_name_Entered.insert(0,vright_turn)
    
def leftFwdSldAction(event):
    global vleft_fwd   
    vleft_fwd=int(vleft_fwd_slider.get())
    vfront_name_Entered.delete(0,tk.END)
    vfront_name_Entered.insert(0,vleft_fwd)
    
def rightFwdSldAction(event):
    global vright_fwd   
    vright_fwd=int(vright_fwd_slider.get())
    rfront_name_Entered.delete(0,tk.END)
    rfront_name_Entered.insert(0,vright_fwd)
    
def updateTmapAction():
    print(ltmap_wp1_name.get())
    tmap_wp[0]=(ltmap_wp1_name.get(),rtmap_wp1_name.get(),tmap_t1_name.get())
    tmap_wp[1]=(ltmap_wp2_name.get(),rtmap_wp2_name.get(),tmap_t2_name.get())
    tmap_wp[2]=(ltmap_wp3_name.get(),rtmap_wp3_name.get(),tmap_t3_name.get())
    tmap_wp[3]=(ltmap_wp4_name.get(),rtmap_wp4_name.get(),tmap_t4_name.get())
    tmap_wp[4]=(ltmap_wp5_name.get(),rtmap_wp5_name.get(),tmap_t5_name.get())
    tmap_wp[5]=(ltmap_wp6_name.get(),rtmap_wp6_name.get(),tmap_t6_name.get())
    tmap_wp[6]=(ltmap_wp7_name.get(),rtmap_wp7_name.get(),tmap_t7_name.get())
    tmap_wp[7]=(ltmap_wp8_name.get(),rtmap_wp8_name.get(),tmap_t8_name.get())
    tmap_wp[8]=(ltmap_wp9_name.get(),rtmap_wp9_name.get(),tmap_t9_name.get())
    tmap_wp[9]=(ltmap_wp10_name.get(),rtmap_wp10_name.get(),tmap_t10_name.get())
    print(tmap_wp)
def _destroyWindow():
    plot_win.quit()
    plot_win.destroy()
def plotMPUGUI(path):
    print(path)
    l=len(path)
    print(str(l))
    t=np.linspace(0,l,l)
    x_dis=[]
    y_dis=[]
    for i in range(l):
      x_dis.append(path[i][4])
      y_dis.append(path[i][5])
    fig=Figure(figsize=(12,8),facecolor='white')
    axis=fig.add_subplot(211)
    axis.plot(t,y_dis)
    axis.set_xlabel('time')
    axis.set_ylabel('y_dis')
    axis.grid(linestyle='-')
    plot_win.withdraw()
    plot_win.protocol('WM_DELETE_WINDOW',_destroyWindow)
    canvas=FigureCanvasTkAgg(fig,master=plot_win)
    canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
    plot_win.update()
    plot_win.deiconify()
    plot_win.mainloop()
    
def tmapRunAction():
    print("running tmap mode")
    print("with map")
    print(tmap_wp)
    print("total run time of circuit is ")
    netTime=0
    for segment in range(10):
        netTime=netTime+(int(tmap_wp[segment][2]))
    print("total run time of circuit is "+str(netTime))
    if(accPlotEn):
        print("calling MPU")
        a_path={}
        iMPU()
        temp()
        runMPU(a_path,netTime)
        #process=Thread(target=runMPU,args=[mpuPath,netTime])
        #process.start()
        #threads.append(process)
        #runMPU(mpuPath,netTime)
    for segment in range(10):
        print("cmd ********************************"+str(segment))
        sendSerCmd('v=l'+str(tmap_wp[segment][0])+'r'+str(tmap_wp[segment][1])+'z/r/n')
        time.sleep(int(tmap_wp[segment][2]))
    print("exiting tmap mode by calling stop button")
    sendSerCmd('v=l0r0z/r/n')
    for process in threads:
        process.join()
        print("thread done")
    if(accPlotEn):
        plotData(mpuPath,0.1)
        plotMPUGUI(mpuPath)
try:
    manualFrame=ttk.LabelFrame(win,text="Manual control")
    manualFrame.grid(column=0,row=2)
    alabel=ttk.Label(win,text="A label")
    alabel.grid(column=0,row=0)
    ttk.Label(manualFrame,text=" ").grid(column=0,row=6)
    ttk.Label(manualFrame,text=" ").grid(column=0,row=7)
    
    #LABELS
    ttk.Label(manualFrame,text="right_turn").grid(column=0,row=8)

    ttk.Label(manualFrame,text="left_turn").grid(column=1,row=8)    

    ttk.Label(manualFrame,text="vel_left_front").grid(column=2,row=8)
    
    ttk.Label(manualFrame,text="vel_right_front").grid(column=3,row=8)
    
    #manual velocities
    vleft_turn_name=tk.StringVar()
    vleft_turn_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vleft_turn_name)
    vleft_turn_name_Entered.grid(column=0,row=9)
    
    vright_turn_name=tk.StringVar()
    vright_turn_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vright_turn_name)
    vright_turn_name_Entered.grid(column=1,row=9)
    
    vfront_name=tk.StringVar()
    vfront_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vfront_name)
    vfront_name_Entered.grid(column=2,row=9)
    
    rfront_name=tk.StringVar()
    rfront_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=rfront_name)
    rfront_name_Entered.grid(column=3,row=9)
    
   
    vel_updt_btn=ttk.Button(manualFrame,text="UpdateVelocity via text",command=velUpdateAction)
    vel_updt_btn.grid(column=5,row=9)
    
    #vel_sld_updt_btn=ttk.Button(manualFrame,text="Update Vel via slider",command=velUpdateSldAction)
    #vel_sld_updt_btn.grid(column=5,row=9)
    
    hwrst_btn=ttk.Button(manualFrame,text="Hard Reset",command=hwrstAction)
    hwrst_btn.grid(column=5,row=0)
    
    swrst_btn=ttk.Button(manualFrame,text="Soft Reset",command=swrstAction)
    swrst_btn.grid(column=6,row=0)
    
    lf_btn=ttk.Button(manualFrame,text="Left",command=leftAction)
    lf_btn.grid(column=1,row=4)
    
    rt_btn=ttk.Button(manualFrame,text="Right",command=rightAction)
    rt_btn.grid(column=3,row=4)
    
    stop_btn=ttk.Button(manualFrame,text="Stop",command=stopAction)
    stop_btn.grid(column=2,row=5)
    
    front_btn=ttk.Button(manualFrame,text="Front",command=frontAction)
    front_btn.grid(column=2,row=3)
    
     #slider velocities
    vleft_turn_slider=tk.Scale(manualFrame,sliderlength=10,from_=0,to=250,orient=tk.HORIZONTAL,command=leftSldAction)
    vleft_turn_slider.grid(column=0,row=11)
    
    vright_turn_slider=tk.Scale(manualFrame,sliderlength=10,from_=0,to=250,orient=tk.HORIZONTAL,command=rightSldAction)
    vright_turn_slider.grid(column=1,row=11)
    
    vleft_fwd_slider=tk.Scale(manualFrame,sliderlength=10,from_=0,to=250,orient=tk.HORIZONTAL,command=leftFwdSldAction)
    vleft_fwd_slider.grid(column=2,row=11)
    
    vright_fwd_slider=tk.Scale(manualFrame,sliderlength=10,from_=0,to=250,orient=tk.HORIZONTAL,command=rightFwdSldAction)
    vright_fwd_slider.grid(column=3,row=11)
    
    ttk.Label(manualFrame,text="  ").grid(column=0,row=12)
    ttk.Label(manualFrame,text="  ").grid(column=0,row=13)
    ttk.Label(manualFrame,text="  ").grid(column=0,row=14)
    
    ############################
    ##  TIME BASED ROUTE
    tmapFrame=ttk.LabelFrame(win,text="Time based way points")
    tmapFrame.grid(column=0,row=15)
    
    tk.Label(tmapFrame,text="vel   left").grid(column=1,row=1)
    tk.Label(tmapFrame,text="vel   right").grid(column=2,row=1)
    tk.Label(tmapFrame,text="duration").grid(column=3,row=1)
    tk.Label(tmapFrame,text="segment_1 ").grid(column=0,row=2)
    tk.Label(tmapFrame,text="segment_2 ").grid(column=0,row=3)
    tk.Label(tmapFrame,text="segment_3 ").grid(column=0,row=4)
    tk.Label(tmapFrame,text="segment_4 ").grid(column=0,row=5)
    tk.Label(tmapFrame,text="segment_5 ").grid(column=0,row=6)
    tk.Label(tmapFrame,text="segment_6 ").grid(column=0,row=7)
    tk.Label(tmapFrame,text="segment_7 ").grid(column=0,row=8)
    tk.Label(tmapFrame,text="segment_8 ").grid(column=0,row=9)
    tk.Label(tmapFrame,text="segment_9 ").grid(column=0,row=10)
    tk.Label(tmapFrame,text="segment_10 ").grid(column=0,row=11)

    ltmap_wp1=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp1_name)
    ltmap_wp2=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp2_name)
    ltmap_wp3=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp3_name)
    ltmap_wp4=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp4_name)
    ltmap_wp5=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp5_name)
    ltmap_wp6=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp6_name)
    ltmap_wp7=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp7_name)
    ltmap_wp8=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp8_name)
    ltmap_wp9=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp9_name)
    ltmap_wp10=ttk.Entry(tmapFrame,width=12,textvariable=ltmap_wp10_name)
    
    rtmap_wp1=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp1_name)
    rtmap_wp2=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp2_name)
    rtmap_wp3=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp3_name)
    rtmap_wp4=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp4_name)
    rtmap_wp5=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp5_name)
    rtmap_wp6=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp6_name)
    rtmap_wp7=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp7_name)
    rtmap_wp8=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp8_name)
    rtmap_wp9=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp9_name)
    rtmap_wp10=ttk.Entry(tmapFrame,width=12,textvariable=rtmap_wp10_name)
    
    
    tmap_t1=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t1_name)
    tmap_t2=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t2_name)
    tmap_t3=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t3_name)
    tmap_t4=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t4_name)
    tmap_t5=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t5_name)
    tmap_t6=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t6_name)
    tmap_t7=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t7_name)
    tmap_t8=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t8_name)
    tmap_t9=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t9_name)
    tmap_t10=ttk.Entry(tmapFrame,width=12,textvariable=tmap_t10_name)
    
    ltmap_wp1.grid(column=1,row=2)
    ltmap_wp2.grid(column=1,row=3)
    ltmap_wp3.grid(column=1,row=4)
    ltmap_wp4.grid(column=1,row=5)
    ltmap_wp5.grid(column=1,row=6)
    ltmap_wp6.grid(column=1,row=7)
    ltmap_wp7.grid(column=1,row=8)
    ltmap_wp8.grid(column=1,row=9)
    ltmap_wp9.grid(column=1,row=10)
    ltmap_wp10.grid(column=1,row=11)
    
    
    rtmap_wp1.grid(column=2,row=2)
    rtmap_wp2.grid(column=2,row=3)
    rtmap_wp3.grid(column=2,row=4)
    rtmap_wp4.grid(column=2,row=5)
    rtmap_wp5.grid(column=2,row=6)
    rtmap_wp6.grid(column=2,row=7)
    rtmap_wp7.grid(column=2,row=8)
    rtmap_wp8.grid(column=2,row=9)
    rtmap_wp9.grid(column=2,row=10)
    rtmap_wp10.grid(column=2,row=11)
    
    tmap_t1.grid(column=3,row=2)
    tmap_t2.grid(column=3,row=3)
    tmap_t3.grid(column=3,row=4)
    tmap_t4.grid(column=3,row=5)
    tmap_t5.grid(column=3,row=6)
    tmap_t6.grid(column=3,row=7)
    tmap_t7.grid(column=3,row=8)
    tmap_t8.grid(column=3,row=9)
    tmap_t9.grid(column=3,row=10)
    tmap_t10.grid(column=3,row=11)
    
    update_tmap_btn=ttk.Button(tmapFrame,text="UpdateTMAP",command=updateTmapAction)
    update_tmap_btn.grid(column=6,row=5)
    tmap_run_btn=ttk.Button(tmapFrame,text="Start TMAP run",command=tmapRunAction)
    tmap_run_btn.grid(column=8,row=6)
    
    ############################
    ##  TIME BASED ROUTE
    dvmapFrame=ttk.LabelFrame(win,text="Velocity based way points")
    dvmapFrame.grid(column=0,row=16)
    
    tk.Label(dvmapFrame,text="ICR   ").grid(column=1,row=1)
    tk.Label(dvmapFrame,text="Distance").grid(column=2,row=1)
    tk.Label(dvmapFrame,text="ICR   ").grid(column=4,row=1)
    tk.Label(dvmapFrame,text="Distance").grid(column=5,row=1)
    tk.Label(dvmapFrame,text="segment_1 ").grid(column=0,row=2)
    tk.Label(dvmapFrame,text="segment_2 ").grid(column=0,row=3)
    tk.Label(dvmapFrame,text="segment_3 ").grid(column=0,row=4)
    tk.Label(dvmapFrame,text="segment_4 ").grid(column=0,row=5)
    tk.Label(dvmapFrame,text="segment_5 ").grid(column=0,row=6)
    tk.Label(dvmapFrame,text="segment_6 ").grid(column=3,row=2)
    tk.Label(dvmapFrame,text="segment_7 ").grid(column=3,row=3)
    tk.Label(dvmapFrame,text="segment_8 ").grid(column=3,row=4)
    tk.Label(dvmapFrame,text="segment_9 ").grid(column=3,row=5)
    tk.Label(dvmapFrame,text="segment_10 ").grid(column=3,row=6)
    
    icrmap_wp1=ttk.Entry(dvmapFrame,width=12,textvariable=icr1)
    icrmap_wp2=ttk.Entry(dvmapFrame,width=12,textvariable=icr2)
    icrmap_wp3=ttk.Entry(dvmapFrame,width=12,textvariable=icr3)
    icrmap_wp4=ttk.Entry(dvmapFrame,width=12,textvariable=icr4)
    icrmap_wp5=ttk.Entry(dvmapFrame,width=12,textvariable=icr5)
    icrmap_wp6=ttk.Entry(dvmapFrame,width=12,textvariable=icr6)
    icrmap_wp7=ttk.Entry(dvmapFrame,width=12,textvariable=icr7)
    icrmap_wp8=ttk.Entry(dvmapFrame,width=12,textvariable=icr8)
    icrmap_wp9=ttk.Entry(dvmapFrame,width=12,textvariable=icr9)
    icrmap_wp10=ttk.Entry(dvmapFrame,width=12,textvariable=icr10)
    
    icrmap_wp1.grid(column=1,row=2)
    icrmap_wp2.grid(column=1,row=3)
    icrmap_wp3.grid(column=1,row=4)
    icrmap_wp4.grid(column=1,row=5)
    icrmap_wp5.grid(column=1,row=6)
    icrmap_wp6.grid(column=4,row=2)
    icrmap_wp7.grid(column=4,row=3)
    icrmap_wp8.grid(column=4,row=4)
    icrmap_wp9.grid(column=4,row=5)
    icrmap_wp10.grid(column=4,row=6)
    
    dismap_wp1=ttk.Entry(dvmapFrame,width=12,textvariable=dis1)
    dismap_wp2=ttk.Entry(dvmapFrame,width=12,textvariable=dis2)
    dismap_wp3=ttk.Entry(dvmapFrame,width=12,textvariable=dis3)
    dismap_wp4=ttk.Entry(dvmapFrame,width=12,textvariable=dis4)
    dismap_wp5=ttk.Entry(dvmapFrame,width=12,textvariable=dis5)
    dismap_wp6=ttk.Entry(dvmapFrame,width=12,textvariable=dis6)
    dismap_wp7=ttk.Entry(dvmapFrame,width=12,textvariable=dis7)
    dismap_wp8=ttk.Entry(dvmapFrame,width=12,textvariable=dis8)
    dismap_wp9=ttk.Entry(dvmapFrame,width=12,textvariable=dis9)
    dismap_wp10=ttk.Entry(dvmapFrame,width=12,textvariable=dis10)
    
    dismap_wp1.grid(column=2,row=2)
    dismap_wp2.grid(column=2,row=3)
    dismap_wp3.grid(column=2,row=4)
    dismap_wp4.grid(column=2,row=5)
    dismap_wp5.grid(column=2,row=6)
    dismap_wp6.grid(column=5,row=2)
    dismap_wp7.grid(column=5,row=3)
    dismap_wp8.grid(column=5,row=4)
    dismap_wp9.grid(column=5,row=5)
    dismap_wp10.grid(column=5,row=6)
    
    update_dvmap_btn=ttk.Button(dvmapFrame,text="UpdateDMAP",command=updateTmapAction)
    update_dvmap_btn.grid(column=6,row=3)
    dvmap_run_btn=ttk.Button(dvmapFrame,text="Start DMAP run",command=tmapRunAction)
    dvmap_run_btn.grid(column=7,row=4)
    win.mainloop()
    #plot_win.mainloop()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
