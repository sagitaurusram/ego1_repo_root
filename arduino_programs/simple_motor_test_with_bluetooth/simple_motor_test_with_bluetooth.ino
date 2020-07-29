
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



void run_all_motorsfwd(){
  motor_cmd(MOTOR1,1,0,125);
  motor_cmd(MOTOR2,1,0,125);
  motor_cmd(MOTOR3,1,0,125);
  motor_cmd(MOTOR4,1,0,125);
  delay(5000);
  stop_all();
}
void run_all_motorsrev(){
  motor_cmd(MOTOR1,1,150,0);
  motor_cmd(MOTOR2,1,150,0);
  motor_cmd(MOTOR3,1,150,0);
  motor_cmd(MOTOR4,1,150,0);
  delay(5000);
  stop_all();
}
void loop() {
  char inp;
  
if (Serial3.available()) /* If data is available on serial port */
    {
      
      inp=Serial3.read();
      flag=~flag;
     Serial.write(inp); /* Print character received on to the serial monitor */
     if(inp=='1'){
      Serial.write("MOTOR1");
      test_single_motor(MOTOR1);
      Serial.write("done");
    // pwm(HIGH,LOW,LOW,LOW);
    }
    else if (inp=='2'){
      Serial.write("MOTOR2");
      test_single_motor(MOTOR2);
      Serial.write("done");
    //  pwm(LOW,HIGH,LOW,LOW);
    }
    else if (inp=='3'){
      Serial.write("MOTOR3");
      test_single_motor(MOTOR3);
      Serial.write("done");
     // pwm(HIGH,LOW,HIGH,LOW);
    }
    else if(inp=='4'){
    Serial.write("MOTOR4");
    test_single_motor(MOTOR4);
    Serial.write("done");
    //pwm(HIGH,LOW,LOW,HIGH);
    }
    else if(inp=='f'){
    Serial.write("all");
    run_all_motorsfwd();
    Serial.write("done");
    //pwm(HIGH,LOW,LOW,HIGH);
    }
    else if(inp=='r'){
    Serial.write("pause");
    run_all_motorsrev();
    Serial.write("done");
    //pwm(HIGH,LOW,LOW,HIGH);
    }
    }
     
}
