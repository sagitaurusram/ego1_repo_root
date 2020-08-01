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
import mpu as mpu;
'''
MPU settings
'''

threads=[]


bus,xCal,yCal=mpu.iMPU()


win=tk.Tk()
win.title("EGO gui")


plot_win=tk.Tk()
plot_win.title("Sensor plots")


auto=1
SERIAL_EN=1
if SERIAL_EN:
    ser1=serial.Serial('/dev/ttyUSB0',38400)
    print(ser1.name)
    time.sleep(1)
    ser1.write('GET Kpr\n'.encode())
    time.sleep(1)
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
process=Thread(target=read,args=[ser1])
process.start()
time.sleep(1)

mpuPath={}
  
vleft_turn=0
vright_turn=0
vleft_fwd=0
vright_fwd=0
ticks=0
time0_dist1=0
vleft_turn_name=tk.StringVar(value=0.1)
vright_turn_name=tk.StringVar(value=0.2)
vfront_name=tk.StringVar(value=0)
ticks_name=tk.StringVar(value=5000)
time0_dist1_name=tk.StringVar(value=0)
#waypoints
tmap_wp=[]
for i in range(10):
    tmap_wp.append((0,0,0))
ltmap_wp1_name=tk.StringVar(value=0)
ltmap_wp2_name=tk.StringVar(value=0.1)
ltmap_wp3_name=tk.StringVar(value=0)
ltmap_wp4_name=tk.StringVar(value=0.2)
ltmap_wp5_name=tk.StringVar(value=0)
ltmap_wp6_name=tk.StringVar(value=0)
ltmap_wp7_name=tk.StringVar(value=0)
ltmap_wp8_name=tk.StringVar(value=0)
ltmap_wp9_name=tk.StringVar(value=0)
ltmap_wp10_name=tk.StringVar(value=0)

rtmap_wp1_name=tk.StringVar(value=0)
rtmap_wp2_name=tk.StringVar(value=1)
rtmap_wp3_name=tk.StringVar(value=0)
rtmap_wp4_name=tk.StringVar(value=2)
rtmap_wp5_name=tk.StringVar(value=0)
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

w1l_name=tk.StringVar(value=99)
w2l_name=tk.StringVar(value=99)
w3l_name=tk.StringVar(value=99)
w1r_name=tk.StringVar(value=99)
w2r_name=tk.StringVar(value=99)
w3r_name=tk.StringVar(value=99)

print(GPIO.RPI_INFO)
GPIO.setmode(GPIO.BCM)
arduinoHwrstPin=23
GPIO.setup(arduinoHwrstPin,GPIO.OUT,initial=1)

def hwrstAction():
    print("Hard Reset clicked")
    GPIO.output(arduinoHwrstPin,GPIO.LOW)
    time.sleep(0.25)
    GPIO.output(arduinoHwrstPin,GPIO.HIGH)
    time.sleep(2)
    print("Hard Reset released")
    
def sendSerCmd(cmd):
    if SERIAL_EN:
        print("in send SerCmd")
        print(cmd)
        ser1.write(cmd.encode())
        time.sleep(1)
def setKpr(val,sign):
    print("in setKpr")
    print(val)
    cmd=''
    cmd='SET Kpr '
    if sign:
        cmd=cmd+'-'
    cmd=cmd+str(val)+'\n'
    sendSerCmd(cmd)
    time.sleep(1)
        #ser1.write('v=l0r0z/r/n'.encode())
def rightAction():
    global vright_turn
    global time0_dist1
    hwrstAction()
    setKpr(vright_turn,0)
    print("right clicked")
    if int(time0_dist1)==1:
        sendSerCmd('M2 F '+str(ticks)+'\n')
    else:
        sendSerCmd('M1 F '+str(ticks)+'\n')
    
def leftAction():
    global vleft_turn
    global time0_dist1
    print("left clicked")
    hwrstAction()
    setKpr(vleft_turn,1)
    if int(time0_dist1)==1:
        sendSerCmd('M2 F '+str(ticks)+'\n')
    else:
        sendSerCmd('M1 F '+str(ticks)+'\n')
    
def frontAction():
    global vleft_fwd
    global vright_fwd
    global ticks
    global time0_dist1
    hwrstAction()
    setKpr(vleft_fwd,0)
    print("front clicked")
    if int(time0_dist1)==1:
        sendSerCmd('M2 F '+str(ticks)+'\n')
    else:
        sendSerCmd('M1 F '+str(ticks)+'\n')
def revAction():
    global vleft_fwd
    global vright_fwd
    global ticks
    hwrstAction()
    setKpr(vleft_fwd,0)
    print("front clicked")
    sendSerCmd('M2 R '+str(ticks)+'\n')
def getSerCmd(cmd):
    if SERIAL_EN:
        print(cmd)
        ser1.write(cmd.encode())
        line=' '
        while 'Ok' not in str(line):
            line=ser1.readline()
            print(line)
        time.sleep(1)
    
def stopAction():
    print("stop clicked")
    hwrstAction()
def wo1Action():
    print("get wheel odo clicked")
    val_l=sendAndWaitForResponse('GET counterL\n','-')
    val_r=sendAndWaitForResponse('GET counterR\n','-')
    w1l_name.set(value=val_l)
    w1r_name.set(value=val_r)
def wo2Action():
    print("get wheel odo clicked")
    val_l=sendAndWaitForResponse('GET counterL\n','-')
    val_r=sendAndWaitForResponse('GET counterR\n','-')
    w2l_name.set(value=val_l)
    w2r_name.set(value=val_r)
def wo3Action():
    print("get wheel odo clicked")
    val_l=sendAndWaitForResponse('GET counterL\n','-')
    val_r=sendAndWaitForResponse('GET counterR\n','-')
    w3l_name.set(value=val_l)
    w3r_name.set(value=val_r)
def swrstAction():
    print("Soft Reset clicked")

def velUpdateAction():
    global vleft_turn
    global vright_turn
    global vleft_fwd
    global vright_fwd
    global ticks
    global time0_dist1
    print("Updating velocity ")
    vleft_turn=vleft_turn_name.get()
    print('vleft ;'+vleft_turn)
    vright_turn=vright_turn_name.get()
    print('vright :'+vright_turn)
    vleft_fwd=vfront_name.get()
    print('vfor :'+vleft_fwd)
    ticks=ticks_name.get()
    print('ticks :'+ticks)
    time0_dist1=time0_dist1_name.get()
    print(time0_dist1)


    
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
    process1=Thread(target=mpu.rMPU,args=[bus,xCal,yCal,netTime+5,0.01])
    process1.start()
    time.sleep(2)
    sfx=''
    if(int(time0_dist1)==0):
        sfx='M1'
    else:
        sfx='M2'
    for segment in range(10):
        print("cmd ********************************"+str(segment))
        if int(tmap_wp[segment][2])>0:
            if(int(tmap_wp[segment][1])==1):
                sendAndWaitForResponse('SET Kpr -'+str(tmap_wp[segment][0])+'\n','OK')
            elif(int(tmap_wp[segment][1])==2):
                sendAndWaitForResponse('SET Kpr '+str(tmap_wp[segment][0])+'\n','OK')
            else:
                print("going st")
                sendAndWaitForResponse('SET Kpr 0\n','OK')
            sendAndWaitForResponse(sfx+' F '+str(tmap_wp[segment][2])+'000\n','Ended')
    print("exiting tmap mode by calling stop button")
    for process in threads:
        process.join()
        print("thread done")
        process1.join()
try:
    manualFrame=ttk.LabelFrame(win,text="Manual control")
    manualFrame.grid(column=0,row=2)

    #LABELS
    ttk.Label(manualFrame,text="right_turn").grid(column=2,row=3)
    ttk.Label(manualFrame,text="left_turn").grid(column=0,row=3)    
    ttk.Label(manualFrame,text="fwd").grid(column=1,row=3)
    ttk.Label(manualFrame,text="duration/distance").grid(column=3,row=3)
    ttk.Label(manualFrame,text="time0_dist1").grid(column=4,row=3)
    #manual velocities
    
    vleft_turn_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vleft_turn_name)
    vleft_turn_name_Entered.grid(column=0,row=4)
    
    vright_turn_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vright_turn_name)
    vright_turn_name_Entered.grid(column=2,row=4)
    
    vfront_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=vfront_name)
    vfront_name_Entered.grid(column=1,row=4)

    
    ticks_name_Entered=ttk.Entry(manualFrame,width=12,textvariable=ticks_name)
    ticks_name_Entered.grid(column=3,row=4)
    
    time0_dist1_Entered=ttk.Entry(manualFrame,width=12,textvariable=time0_dist1_name)
    time0_dist1_Entered.grid(column=4,row=4)
    
    vel_updt_btn=ttk.Button(manualFrame,text="UpdateVelocity",command=velUpdateAction)
    vel_updt_btn.grid(column=7,row=5)
    
    #vel_sld_updt_btn=ttk.Button(manualFrame,text="Update Vel via slider",command=velUpdateSldAction)
    #vel_sld_updt_btn.grid(column=5,row=9)
    
    hwrst_btn=ttk.Button(manualFrame,text="Hard Reset",command=hwrstAction)
    hwrst_btn.grid(column=7,row=6)
    
    front_btn=ttk.Button(manualFrame,text="Front",command=frontAction)
    front_btn.grid(column=1,row=5)
    rev_btn=ttk.Button(manualFrame,text="Reverse",command=revAction)
    rev_btn.grid(column=1,row=7)

    
    lf_btn=ttk.Button(manualFrame,text="Left",command=leftAction)
    lf_btn.grid(column=0,row=6)
    
    rt_btn=ttk.Button(manualFrame,text="Right",command=rightAction)
    rt_btn.grid(column=2,row=6)
    
    
    
    
     
    
    ttk.Label(manualFrame,text="  ").grid(column=0,row=12)
    ttk.Label(manualFrame,text="  ").grid(column=0,row=13)
    ttk.Label(manualFrame,text="  ").grid(column=0,row=14)
    ########################
    ## Wheel odometry##
    whOdoFrame=ttk.LabelFrame(win,text="Wheel OdoMetry")
    whOdoFrame.grid(column=1,row=2)
    ttk.Label(whOdoFrame,text="left").grid(column=1,row=1)
    ttk.Label(whOdoFrame,text="right").grid(column=2,row=1)
    wo1_btn=ttk.Button(whOdoFrame,text="getWheelOdo",command=wo1Action)
    wo1_btn.grid(column=0,row=2)
    wo2_btn=ttk.Button(whOdoFrame,text="getWheelOdo",command=wo2Action)
    wo2_btn.grid(column=0,row=3)
    wo3_btn=ttk.Button(whOdoFrame,text="getWheelOdo",command=wo3Action)
    wo3_btn.grid(column=0,row=4)
    
    w1l_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w1l_name)
    w2l_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w2l_name)
    w3l_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w3l_name)
    w1r_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w1r_name)
    w2r_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w2r_name)
    w3r_name_Entered=ttk.Entry(whOdoFrame,width=6,textvariable=w3r_name)
    w1l_name_Entered.grid(column=1,row=2)
    w2l_name_Entered.grid(column=1,row=3)
    w3l_name_Entered.grid(column=1,row=4)
    w1r_name_Entered.grid(column=2,row=2)
    w2r_name_Entered.grid(column=2,row=3)
    w3r_name_Entered.grid(column=2,row=4)
    ############################
    ##  TIME BASED ROUTE
    tmapFrame=ttk.LabelFrame(win,text="way points")
    tmapFrame.grid(column=0,row=15)
    
    tk.Label(tmapFrame,text="ICR").grid(column=1,row=1)
    tk.Label(tmapFrame,text="left0_right1").grid(column=2,row=1)
    tk.Label(tmapFrame,text="duration/distance").grid(column=3,row=1)
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
    
    update_tmap_btn=ttk.Button(tmapFrame,text="UpdateMAP",command=updateTmapAction)
    update_tmap_btn.grid(column=6,row=5)
    tmap_run_btn=ttk.Button(tmapFrame,text="Start MAP run",command=tmapRunAction)
    tmap_run_btn.grid(column=8,row=6)
    
    

    win.mainloop()
    #plot_win.mainloop()
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
3