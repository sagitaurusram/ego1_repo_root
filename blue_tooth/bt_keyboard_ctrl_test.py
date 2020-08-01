from switchcase import switch
from pynput.keyboard import Key, Listener

import bluetooth, subprocess
target_name = "HC-06"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices: 
    print(bdaddr)
    print(bluetooth.lookup_name( bdaddr ))
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print("found target bluetooth device with address "+ target_address)
else:
    print("could not find target bluetooth device nearby")



# Now, connect in the same way as always with PyBlueZ
try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((target_address,1))
except bluetooth.btcommon.BluetoothError as err:
    # Error handler
    pass
##################################################################################
directions=["FOR","REV"]
states  =["IDLE","FORWARD","REVERSE","TURN_LEFT","TURN_RIGHT","STOP"]
commands=["move_forward","move_reverse","accel","decel""turn_left","turn_right","stop"]
PWM_LOWEST=50
PWM_MAX=150
RPWM_MAX=150
LPWM_MAX=150
PWM_TURN_START=PWM_LOWEST+20
pwm=50
lpwm=50
rpwm=50
direction="FOR"
state="STOP"
cmd="null"
def run_all_motorsfwd():
	tmp="forward,"+str(pwm)+';'
	print("run all motors fwd: "+tmp)
	s.send(tmp)
def run_all_motorsrev():
	tmp="reverse,"+str(pwm)+';'
	print("run all motors rev: "+tmp)
	s.send(tmp)
def turn_left():
	if direction=="FOR":
		tmp="turn,"+str(lpwm)+','+str(rpwm)+';'
		print("turn left in FORWARD direction"+tmp)
		s.send(tmp)
	else:
		tmp="reverse turn,"+str(lpwm)+','+str(rpwm)+';'
		print("turn left in REVERSE direction "+tmp)
		s.send(tmp)
def turn_right():
	if direction=="FOR":
		tmp="turn,"+str(lpwm)+','+str(rpwm)+';'
		print("turn right in FORWARD direction"+tmp)
		s.send(tmp)
	else:
		tmp="reverse turn,"+str(lpwm)+','+str(rpwm)+';'
		print("turn right in REVERSE direction "+tmp)
		s.send(tmp)		

def stop_all_motors():
	print("stop")	
	s.send("stop;")


def increment_pwm():
	global pwm
	pwm= pwm+10 if pwm<PWM_MAX-5 else PWM_MAX

def decrement_pwm():
	global pwm
	pwm= pwm-10 if pwm>10 else 10

def increment_rpwm():
	global rpwm
	rpwm= rpwm+10 if rpwm<RPWM_MAX-5 else RPWM_MAX

def decrement_rpwm():
	global rpwm
	rpwm= rpwm-10 if rpwm>10 else 10

def increment_lpwm():
	global lpwm
	lpwm= lpwm+10 if lpwm<LPWM_MAX-5 else LPWM_MAX

def decrement_lpwm():
	global lpwm
	lpwm= lpwm-10 if lpwm>10 else 10

def forward_p():
	global pwm,lpwm,rpwm,state,cmd,direction
	print("in case , in state forward_p")
	for case in switch(cmd):
		if case("move_forward"):
			break;
		if case("accel"):
			increment_pwm()
			break
		if case("decel"):
			decrement_pwm()
			break
		if case("move_reverse"):
			state="REVERSE"
			direction="REV"
			pwm=PWM_LOWEST
		if case("turn_left"):
			state="TURN_LEFT"
			lpwm=PWM_LOWEST
			rpwm=PWM_TURN_START
			break
		if case("turn_right"):
			state="TURN_RIGHT"
			lpwm=PWM_TURN_START
			rpwm=PWM_LOWEST
			break
		if case("stop"):
			state="STOP"
	else:
		print("unmatched")

def turn_left_p():
	global pwm,lpwm,rpwm,state,cmd	,direction
	print("in case , in state turn_left_p")
	for case in switch(cmd):
		if case("move_forward"):
			state="FORWARD"
			direction="FOR"
			pwm=PWM_LOWEST
			break;
		if case("accel"):
			break
		if case("decel"):
			break
		if case("move_reverse"):
			state="REVERSE"
			direction="REV"
			pwm=PWM_LOWEST
		if case("turn_left"):
			state="TURN_LEFT"
			lpwm=PWM_LOWEST
			increment_rpwm()
			break
		if case("turn_right"):
			state="TURN_RIGHT"
			lpwm=PWM_TURN_START
			rpwm=PWM_LOWEST
			break
		if case("stop"):
			state="STOP"
	else:
		print("unmatched")

def turn_right_p():
	global pwm,lpwm,rpwm,state,cmd,direction
	print("in case , in state turn_right_p")
	for case in switch(cmd):
		if case("move_forward"):
			state="FORWARD"
			direction="FOR"
			pwm=PWM_LOWEST
			break;
		if case("accel"):
			break
		if case("decel"):
			break
		if case("move_reverse"):
			state="REVERSE"
			direction="REV"
			pwm=PWM_LOWEST
		if case("turn_left"):
			state="TURN_LEFT"
			lpwm=PWM_LOWEST
			rpwm=PWM_TURN_START
			break
		if case("turn_right"):
			state="TURN_RIGHT"
			increment_lpwm()
			rpwm=PWM_LOWEST
			break
		if case("stop"):
			state="STOP"
	else:
		print("unmatched")

def reverse_p():
	global pwm,lpwm,rpwm,state,cmd,direction
	print("in case , in state reverse_p")
	for case in switch(cmd):
		if case("move_forward"):
			state="FORWARD"
			direction="FOR"
			pwm=PWM_LOWEST
			break;
		if case("accel"):
			increment_pwm()
			break
		if case("decel"):
			decrement_pwm()
			break
		if case("move_reverse"):
			break
		if case("turn_left"):
			state="TURN_LEFT"
			lpwm=PWM_LOWEST
			rpwm=PWM_TURN_START
			break
		if case("turn_right"):
			state="TURN_RIGHT"
			lpwm=PWM_TURN_START
			rpwm=PWM_LOWEST
			break
		if case("stop"):
			state="STOP"
	else:
		print("unmatched")
def stop_p():
	global pwm,lpwm,rpwm,state,cmd,direction
	print("in case , in state stop_p , rcvd command is "+cmd)
	for case in switch(cmd):
		if case("move_forward"):
			state="FORWARD"
			direction="FOR"
			pwm=PWM_LOWEST
			break;
		if case("accel"):
			break
		if case("decel"):
			break
		if case("move_reverse"):
			state="REVERSE"
			direction="REV"
			pwm=PWM_LOWEST
			break
		if case("turn_left"):
			state="TURN_LEFT"
			lpwm=PWM_LOWEST
			rpwm=PWM_TURN_START
			break
		if case("turn_right"):
			state="TURN_RIGHT"
			lpwm=PWM_TURN_START
			rpwm=PWM_LOWEST
			break
		if case("stop"):
			state="STOP"
	else:
		print("unmatched")

def update_fsm():
	global pwm,lpwm,rpwm,state,cmd
	print("in update fsm , in state :"+state)
	for case in switch(state):
		if case("FORWARD"):
			forward_p()			
			break
		if case("REVERSE"):
			reverse_p()			
			break
		if case("TURN_LEFT"):
			turn_left_p()			
			break
		if case("TURN_RIGHT"):
			turn_right_p()			
			break
		if case("STOP"):
			stop_p()
			break
	else:
		print("x was unmatched")
	print("switched to state "+state)
	
def wait_for_cmd():
	print("waiting for command")
	return input("enter the command : ")

def update_bot():
	print("updating motors")
	print("current parameters")
	print("pwm is "+str(pwm))
	print("lpwm is "+str(lpwm))
	print("rpwm is "+str(rpwm))
	print("direction is "+direction)
	print("state is "+state)
	if   state=="FORWARD":
		run_all_motorsfwd()
	elif state=="REVERSE":
		run_all_motorsrev()
	elif state=="TURN_LEFT":
		turn_left()
	elif state=="TURN_RIGHT":
		turn_right()
	elif state=="STOP":
		stop_all_motors()
	print("---------------------------------------------------")
def on_press(key):
	global cmd
	try:	
		if key== key.up:
			print("move_forward")
			cmd="move_forward"
		elif key==key.down:
			print("move_reverse")
			cmd="move_reverse"
		elif key==key.space:
			cmd="stop"
		elif key==key.left:
			cmd="turn_left"
		elif key==key.right:
			cmd="turn_right"
	except AttributeError:
		print("attribute error")
		if key.char=='a':
			print("accel")
			cmd="accel"
		elif key.char=='d':
			print("decel")
			cmd="decel"
	#cmd=wait_for_cmd()
	update_fsm()
	update_bot()

def on_release(key):
	#print('{0} release'.format(key))
	if key == Key.esc:
        # Stop listener
		cmd="stop"
		return False

# Collect events until released

print("starting")
state="STOP"
	
with Listener(on_press=on_press,on_release=on_release) as listener:
	listener.join()




