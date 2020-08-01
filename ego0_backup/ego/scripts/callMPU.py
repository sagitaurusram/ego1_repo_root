import mpu as mpu;
from threading import Thread

bus,xCal,yCal=mpu.iMPU()
process1=Thread(target=mpu.rMPU,args=[bus,xCal,yCal,6,0.1])
process1.start()
time.sleep(1)

process1.join()

