#define MOTOR2 2
#define EN_PIN_M2 47
#define FPWM_PIN_M2 12
#define RPWM_PIN_M2 13

#define MOTOR3 3
#define EN_PIN_M3 45
#define FPWM_PIN_M3 11
#define RPWM_PIN_M3 10

#define MOTOR1 1
#define EN_PIN_M1 26
#define FPWM_PIN_M1 5
#define RPWM_PIN_M1 4

#define MOTOR4 4
#define EN_PIN_M4 28
#define FPWM_PIN_M4 3
#define RPWM_PIN_M4 2

#include<SoftwareSerial.h>
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
 
 Serial.write("hello");
/*
digitalWrite(EN_PIN,HIGH);
analogWrite(FPWM_PIN,0);
analogWrite(RPWM_PIN,125);*/
}
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
void motor_cmd_DC(int motor){
  int enb_pin,for_pwm_pin,rev_pwm_pin;
    switch(motor){
    case MOTOR1 : enb_pin=EN_PIN_M1; for_pwm_pin=FPWM_PIN_M1; rev_pwm_pin=RPWM_PIN_M1; break;
    case MOTOR2 : enb_pin=EN_PIN_M2; for_pwm_pin=FPWM_PIN_M2; rev_pwm_pin=RPWM_PIN_M2; break;
    case MOTOR3 : enb_pin=EN_PIN_M3; for_pwm_pin=FPWM_PIN_M3; rev_pwm_pin=RPWM_PIN_M3; break;
    case MOTOR4 : enb_pin=EN_PIN_M4; for_pwm_pin=FPWM_PIN_M4; rev_pwm_pin=RPWM_PIN_M4; break;
    default     : break;
  }
  digitalWrite( enb_pin,HIGH);
  digitalWrite( for_pwm_pin, HIGH);
  digitalWrite( rev_pwm_pin, HIGH);
  
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

void test_DC(){
  motor_cmd_DC(MOTOR1);
  motor_cmd_DC(MOTOR2);
  motor_cmd_DC(MOTOR3);
  motor_cmd_DC(MOTOR4);
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
 /* digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(2000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000); */                      // wait for a second
  
  // put your main code here, to run repeatedly:
 /* test_single_motor(MOTOR1);
  test_single_motor(MOTOR2);
  test_single_motor(MOTOR3);
  test_single_motor(MOTOR4);*/
  /*
run_all_motorsfwd();
   run_all_motorsrev();*/
  
  
if (Serial.available()) /* If data is available on serial port */
    {
      
      inp=Serial.read();
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
    else if(inp=='a'){
    Serial.write("all");
    run_all_motorsfwd();
    Serial.write("done");
    //pwm(HIGH,LOW,LOW,HIGH);
    }
    else if(inp=='p'){
    Serial.write("pause");
    run_all_motorsrev();
    Serial.write("done");
    //pwm(HIGH,LOW,LOW,HIGH);
    }
    }
     
}
