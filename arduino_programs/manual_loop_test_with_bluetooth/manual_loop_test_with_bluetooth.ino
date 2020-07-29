
#include<SoftwareSerial.h>
#include "arduino_connections.h"
#include "motor_control.c"

bool flag=true;
/* Create object named bt of the class SoftwareSerial */ 
//SoftwareSerial bt(15,14); /* (Rx,Tx) */  
void setup() {
  // put your setup code here, to run once:
pinMode(LED_BUILTIN, OUTPUT);
pinMode(EN_PIN_M1, OUTPUT);
pinMode(FPWM_PIN_M1, OUTPUT);
pinMode(RPWM_PIN_M1, OUTPUT);
pinMode(EN_PIN_M2, OUTPUT);
pinMode(FPWM_PIN_M2, OUTPUT);
pinMode(RPWM_PIN_M2, OUTPUT);
pinMode(EN_PIN_M3, OUTPUT);
pinMode(FPWM_PIN_M3, OUTPUT);
pinMode(RPWM_PIN_M3, OUTPUT);
pinMode(EN_PIN_M4, OUTPUT);
pinMode(FPWM_PIN_M4, OUTPUT);
pinMode(RPWM_PIN_M4, OUTPUT);
 //bt.begin(9600); /* Define baud rate for software serial communication */
 Serial.begin(9600); /* Define baud rate for serial communication */
 Serial3.begin(9600);
 Serial.write("hello");
}


void loop() {
  char inp;
  int l_pwm,r_pwm;
  int f_pwm,b_pwm;
if (Serial3.available()) /* If data is available on serial port */
    {
      inp=Serial3.read();
      flag=~flag;
     Serial.write("cmd rxd:");
     Serial.write(inp); /* Print character received on to the serial monitor */
     switch(inp){
      case '1' :Serial.write("test motor1");test_single_motor(MOTOR1); break;
      case '2' :Serial.write("test motor2");test_single_motor(MOTOR2); break;
      case '3' :Serial.write("test motor3");test_single_motor(MOTOR3); break;
      case '4' :Serial.write("test motor4");test_single_motor(MOTOR4); break;
      case 'l' :Serial.write("left turn");  turn_left(100,50);               break;
      case 'r' :Serial.write("right turn"); turn_right(50,100);              break;
      case 'f' :Serial.write("forward");    run_all_motorsfwd(100);       break;
      case 'b' :Serial.write("backward");   run_all_motorsrev(100);       break;
      case 's' :Serial.write("stop all");   stop_all();                break;
      default  : break; 
     }
     Serial.write("done");
    }
     
}
