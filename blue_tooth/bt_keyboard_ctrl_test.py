from switchcase import switch

directions=["FOR","REV"]
states  =["IDLE","FORWARD","REVERSE","TURN_LEFT","TURN_RIGHT","STOP"]
commands=["move_forward","move_reverse","accel","decel""turn_left","turn_right","stop"]
PWM_LOWEST=50
PWM_TURN_START=100
pwm=50
lpwm=50
rpwm=50
direction="FOR"
state="STOP"
cmd="null"
def run_all_motorsfwd():
	print("run all motors fwd")

def run_all_motorsrev():
	print("run all motors rev")

def turn_left():
	
	if direction=="FOR":
		print("turn left in FORWARD direction")
	else:
		print("turn left in REVERSE direction ")

def turn_right():
	if direction=="FOR":
		print("turn right in FORWARD direction")
	else:
		print("turn right in REVERSE direction ")		

def stop_all_motors():
	print("stop")	



def forward_p():
	global pwm,lpwm,rpwm,state,cmd,direction
	print("in case , in state forward_p")
	for case in switch(cmd):
		if case("move_forward"):
			break;
		if case("accel"):
			pwm=pwm+10
			break
		if case("decel"):
			pwm=pwm-10
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
			rpwm=rpwm+10
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
			lpwm=lpwm+10
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
			pwm=pwm+10
			break
		if case("decel"):
			pwm=pwm-10
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
	print("in case , in state stop_p")
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

print("starting")
state="STOP"
while True:
	cmd=wait_for_cmd()
	update_fsm()
	update_bot()





