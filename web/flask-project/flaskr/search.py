from switchcase import switch


class BotController:
    directions = ["FOR", "REV"]
    states = ["IDLE", "FORWARD", "REVERSE", "TURN_LEFT", "TURN_RIGHT", "STOP"]
    commands = ["move_forward", "move_reverse", "accelerate", "decelerate""turn_left", "turn_right", "stop"]
    PWM_LOWEST = 50
    PWM_MAX = 150
    RIGHT_PWM_MAX = 150
    LEFT_PWM_MAX = 150
    PWM_TURN_START = PWM_LOWEST + 20
    pwm = 50
    left_pwm = 50
    right_pwm = 50
    direction = "FOR"
    state = "STOP"
    cmd = "null"
    debug_mode = 0
    cmd_to_send = ""

    def run_all_motors_forward(self):
        tmp = "forward," + str(self.pwm) + ';'
        print("run all motors fwd: " + tmp)
        self.cmd_to_send = tmp

    def run_all_motors_reverse(self):
        tmp = "reverse," + str(self.pwm) + ';'
        print("run all motors rev: " + tmp)
        self.cmd_to_send = tmp

    def turn_left(self):
        if self.direction == "FOR":
            tmp = "turn," + str(self.left_pwm) + ',' + str(self.right_pwm) + ';'
            print("turn left in FORWARD direction" + tmp)
            self.cmd_to_send = tmp
        else:
            tmp = "reverse turn," + str(self.left_pwm) + ',' + str(self.right_pwm) + ';'
            print("turn left in REVERSE direction " + tmp)
            self.cmd_to_send = tmp

    def turn_right(self):
        if self.direction == "FOR":
            tmp = "turn," + str(self.left_pwm) + ',' + str(self.right_pwm) + ';'
            print("turn right in FORWARD direction" + tmp)
            self.cmd_to_send = tmp
        else:
            tmp = "reverse turn," + str(self.left_pwm) + ',' + str(self.right_pwm) + ';'
            print("turn right in REVERSE direction " + tmp)
            self.cmd_to_send = tmp

    def stop_all_motors(self):
        print("stop")
        self.cmd_to_send = "stop;"

    def increment_pwm(self):
        self.pwm = self.pwm + 10 if self.pwm < self.PWM_MAX - 5 else self.PWM_MAX

    def decrement_pwm(self):
        self.pwm = self.pwm - 10 if self.pwm > 10 else 10

    def increment_rpwm(self):
        self.right_pwm = self.right_pwm + 10 if self.right_pwm < self.RIGHT_PWM_MAX - 5 else self.RIGHT_PWM_MAX

    def decrement_rpwm(self):
        self.right_pwm = self.right_pwm - 10 if self.right_pwm > 10 else 10

    def increment_lpwm(self):
        self.left_pwm = self.left_pwm + 10 if self.left_pwm < self.LEFT_PWM_MAX - 5 else self.LEFT_PWM_MAX

    def decrement_lpwm(self):
        self.left_pwm = self.left_pwm - 10 if self.left_pwm > 10 else 10

    def forward_p(self):
        print("in case , in state forward_p")
        for case in switch(self.cmd):
            if case("move_forward"):
                break
            if case("accelerate"):
                self.increment_pwm()
                break
            if case("decelerate"):
                self.decrement_pwm()
                break
            if case("move_reverse"):
                self.state = "REVERSE"
                self.direction = "REV"
                self.pwm = self.PWM_LOWEST
            if case("turn_left"):
                self.state = "TURN_LEFT"
                self.left_pwm = self.PWM_LOWEST
                self.right_pwm = self.PWM_TURN_START
                break
            if case("turn_right"):
                self.state = "TURN_RIGHT"
                self.left_pwm = self.PWM_TURN_START
                self.right_pwm = self.PWM_LOWEST
                break
            if case("stop"):
                self.state = "STOP"
        else:
            print("unmatched")

    def turn_left_p(self):
        print("in case , in state turn_left_p")
        for case in switch(self.cmd):
            if case("move_forward"):
                self.state = "FORWARD"
                self.direction = "FOR"
                self.pwm = self.PWM_LOWEST
                break
            if case("accelerate"):
                break
            if case("decelerate"):
                break
            if case("move_reverse"):
                self.state = "REVERSE"
                self.direction = "REV"
                self.pwm = self.PWM_LOWEST
            if case("turn_left"):
                self.state = "TURN_LEFT"
                self.left_pwm = self.PWM_LOWEST
                self.increment_rpwm()
                break
            if case("turn_right"):
                self.state = "TURN_RIGHT"
                self.left_pwm = self.PWM_TURN_START
                self.right_pwm = self.PWM_LOWEST
                break
            if case("stop"):
                self.state = "STOP"
        else:
            print("unmatched")

    def turn_right_p(self):
        print("in case , in state turn_right_p")
        for case in switch(self.cmd):
            if case("move_forward"):
                self.state = "FORWARD"
                self.direction = "FOR"
                self.pwm = self.PWM_LOWEST
                break
            if case("accelerate"):
                break
            if case("decelerate"):
                break
            if case("move_reverse"):
                self.state = "REVERSE"
                self.direction = "REV"
                self.pwm = self.PWM_LOWEST
            if case("turn_left"):
                self.state = "TURN_LEFT"
                self.left_pwm = self.PWM_LOWEST
                self.right_pwm = self.PWM_TURN_START
                break
            if case("turn_right"):
                self.state = "TURN_RIGHT"
                self.increment_lpwm()
                self.right_pwm = self.PWM_LOWEST
                break
            if case("stop"):
                self.state = "STOP"
        else:
            print("unmatched")

    def reverse_p(self):
        print("in case , in state reverse_p")
        for case in switch(self.cmd):
            if case("move_forward"):
                self.state = "FORWARD"
                self.direction = "FOR"
                self.pwm = self.PWM_LOWEST
                break
            if case("accelerate"):
                self.increment_pwm()
                break
            if case("decelerate"):
                self.decrement_pwm()
                break
            if case("move_reverse"):
                break
            if case("turn_left"):
                self.state = "TURN_LEFT"
                self.left_pwm = self.PWM_LOWEST
                self.right_pwm = self.PWM_TURN_START
                break
            if case("turn_right"):
                self.state = "TURN_RIGHT"
                self.left_pwm = self.PWM_TURN_START
                self.right_pwm = self.PWM_LOWEST
                break
            if case("stop"):
                self.state = "STOP"
        else:
            print("unmatched")

    def stop_p(self):
        print("in case , in state stop_p , rcvd command is " + self.cmd)
        for case in switch(self.cmd):
            if case("move_forward"):
                self.state = "FORWARD"
                self.direction = "FOR"
                self.pwm = self.PWM_LOWEST
                break
            if case("accelerate"):
                break
            if case("decelerate"):
                break
            if case("move_reverse"):
                self.state = "REVERSE"
                self.direction = "REV"
                self.pwm = self.PWM_LOWEST
                break
            if case("turn_left"):
                self.state = "TURN_LEFT"
                self.left_pwm = self.PWM_LOWEST
                self.right_pwm = self.PWM_TURN_START
                break
            if case("turn_right"):
                self.state = "TURN_RIGHT"
                self.left_pwm = self.PWM_TURN_START
                self.right_pwm = self.PWM_LOWEST
                break
            if case("stop"):
                self.state = "STOP"
        else:
            print("unmatched")

    def update_fsm(self):
        print("in update fsm , in state :" + self.state)
        for case in switch(self.state):
            if case("FORWARD"):
                self.forward_p()
                break
            if case("REVERSE"):
                self.reverse_p()
                break
            if case("TURN_LEFT"):
                self.turn_left_p()
                break
            if case("TURN_RIGHT"):
                self.turn_right_p()
                break
            if case("STOP"):
                self.stop_p()
                break
        else:
            print("x was unmatched")
        print("switched to state " + self.state)

    @staticmethod
    def wait_for_cmd():
        print("waiting for command")
        return input("enter the command : ")

    def update_bot(self):
        print("updating motors")
        print("current parameters")
        print("pwm is " + str(self.pwm))
        print("lpwm is " + str(self.left_pwm))
        print("rpwm is " + str(self.right_pwm))
        print("direction is " + self.direction)
        print("state is " + self.state)
        if self.state == "FORWARD":
            self.run_all_motors_forward()
        elif self.state == "REVERSE":
            self.run_all_motors_reverse()
        elif self.state == "TURN_LEFT":
            self.turn_left()
        elif self.state == "TURN_RIGHT":
            self.turn_right()
        elif self.state == "STOP":
            self.stop_all_motors()
        print("---------------------------------------------------")

    def on_cmd_reception(self, signal):
        self.cmd = signal
        self.update_fsm()
        self.update_bot()

'''
# Collect events until released
print("starting")
bot = BotController()
while True:
    x = bot.wait_for_cmd()
    bot.on_cmd_reception(x)
'''