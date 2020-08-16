#include "Arduino.h"
#include "arduino_connections.h"

void motor_cmd(int motor, int en,int fpwm,int rpwm){
  int enb_pin,for_pwm_pin, rev_pwm_pin;
  if(fpwm > 0 && rpwm > 0)
    return;
  else {
    switch(motor){
    case MOTOR1 : enb_pin=EN_PIN_M1; for_pwm_pin=FPWM_PIN_M1; rev_pwm_pin=RPWM_PIN_M1; break;
    case MOTOR2 : enb_pin=EN_PIN_M2; for_pwm_pin=FPWM_PIN_M2; rev_pwm_pin=RPWM_PIN_M2; break;
    case MOTOR3 : enb_pin=EN_PIN_M3; for_pwm_pin=FPWM_PIN_M3; rev_pwm_pin=RPWM_PIN_M3; break;
    case MOTOR4 : enb_pin=EN_PIN_M4; for_pwm_pin=FPWM_PIN_M4; rev_pwm_pin=RPWM_PIN_M4; break;
    default     : break;
  }
  digitalWrite( enb_pin,en);
  analogWrite( for_pwm_pin, fpwm);
  analogWrite( rev_pwm_pin, rpwm);
  }
}

void stop_all(){
  motor_cmd(MOTOR1,0,0,0);
  motor_cmd(MOTOR2,0,0,0);
  motor_cmd(MOTOR3,0,0,0);
  motor_cmd(MOTOR4,0,0,0);
}

void test_single_motor(int motor){

  motor_cmd(motor,1,0,125);
  delay(2000);
  motor_cmd(motor,1,125,0);
  delay(5000);
  motor_cmd(motor,1,0,125);
  delay(5000);
  motor_cmd(motor,1,225,0);
  delay(5000);
  motor_cmd(motor,1,0,225);
  delay(5000);
  motor_cmd(motor,0,0,0);
  delay(2000);
  stop_all();
}



void run_all_motorsfwd(int pwm){
  motor_cmd(MOTOR1,1,pwm,0);
  motor_cmd(MOTOR2,1,pwm,0);
  motor_cmd(MOTOR3,1,pwm,0);
  motor_cmd(MOTOR4,1,pwm,0);
}

void run_all_motorsrev(int pwm){
  motor_cmd(MOTOR1,1,0,pwm);
  motor_cmd(MOTOR2,1,0,pwm);
  motor_cmd(MOTOR3,1,0,pwm);
  motor_cmd(MOTOR4,1,0,pwm);
}

//motor3 and 4 forms back
//motors 2 and motors 4 are left side when in the car
void turn_left(int l_pwm, int r_pwm){
  motor_cmd(MOTOR1,1,r_pwm,0);
  motor_cmd(MOTOR2,1,l_pwm,0);
  motor_cmd(MOTOR3,1,r_pwm,0);
  motor_cmd(MOTOR4,1,l_pwm,0);
}
void reverse_turn_left(int l_pwm, int r_pwm){
  motor_cmd(MOTOR1,1,0,r_pwm);
  motor_cmd(MOTOR2,1,0,l_pwm);
  motor_cmd(MOTOR3,1,0,r_pwm);
  motor_cmd(MOTOR4,1,0,l_pwm);
}
void turn_right(int l_pwm, int r_pwm){
  /*motor_cmd(MOTOR1,1,50,0);
  motor_cmd(MOTOR2,1,100,0);
  motor_cmd(MOTOR3,1,50,0);
  motor_cmd(MOTOR4,1,100,0);*/
  motor_cmd(MOTOR1,1,r_pwm,0);
  motor_cmd(MOTOR2,1,l_pwm,0);
  motor_cmd(MOTOR3,1,r_pwm,0);
  motor_cmd(MOTOR4,1,l_pwm,0);
}


