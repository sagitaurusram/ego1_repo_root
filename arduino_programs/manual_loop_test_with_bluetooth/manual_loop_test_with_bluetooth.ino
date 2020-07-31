#include <CommandHandler.h>
#include<SoftwareSerial.h>
#include "arduino_connections.h"
#include "motor_control.c"

bool flag=true;
CommandHandler cmdHdl;
/* Create object named bt of the class SoftwareSerial */ 
//SoftwareSerial bt(15,14); /* (Rx,Tx) */  

// This gets set as the default handler, and gets called when no other command matches.
void unrecognized(const char *command) {
  Serial.println("What?");
}

void sayHello() {
  Serial.println("hello sriram");
  run_all_motorsfwd(100);
  delay(2000);
  stop_all();
}
void scmd_forward(){
  double pwm;
  pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("forward argument was: ");
    Serial.print(pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  run_all_motorsfwd(pwm);
}

void scmd_reverse(){
  double pwm;
  pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("forward argument was: ");
    Serial.print(pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  run_all_motorsrev(pwm);
}
void scmd_turn(){
  //int l_pwm,r_pwm;
  double l_pwm,r_pwm;

  l_pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("First argument was: ");
    Serial.print(l_pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  r_pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("First argument was: ");
    Serial.print(r_pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  
    turn_left(l_pwm,r_pwm);
  
}
void scmd_reverse_turn(){
  double l_pwm,r_pwm;

  l_pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("First argument was: ");
    Serial.print(l_pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  r_pwm = cmdHdl.readDoubleArg();
  if (cmdHdl.argOk) {
    Serial.print("First argument was: ");
    Serial.print(r_pwm, 10);
  }
  else {
    Serial.println("No arguments");
    return;
  }
  
    reverse_turn_left(l_pwm,r_pwm);
  
}
void scmd_stop(){
  stop_all();
}
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

 // Setup callbacks for SerialCommand commands
  cmdHdl.addCommand("HELLO", sayHello);        // Echos the string argument back
  cmdHdl.addCommand("turn", scmd_turn);
  cmdHdl.addCommand("stop", scmd_stop);
  cmdHdl.addCommand("forward", scmd_forward);
  cmdHdl.addCommand("reverse", scmd_reverse);
  cmdHdl.addCommand("reverse turn", scmd_reverse_turn);

  cmdHdl.setDefaultHandler(unrecognized);      // Handler for command that isn't matched  (says "What?")

  cmdHdl.setCmdHeader("ARDUINO"); // here we call it FEEDBACK, a delim will automatically be added after the header
  // use cmdHdl.setCmdHeader("FEEDBACK", false); if you do not want a delimiter

  // always start by initiating your message, it just set things up
  cmdHdl.initCmd();
  // now create the message you like
  cmdHdl.addCmdString("ALIVE"); // add a string
  cmdHdl.addCmdDelim(); // add a delim
  cmdHdl.addCmdBool(true); // add a boolean
  cmdHdl.addCmdDelim(); // add a delim
  cmdHdl.addCmdLong(938); //add a int32
  cmdHdl.addCmdDelim(); // add a delim
  cmdHdl.addCmdDouble(-2147.483647, 3); // add a double, printed with 3 decimal
  // if unspecified decimal, default is 2)
  // you can change the default decimal to N using cmdHdl.setCmdDecimal(N)
  cmdHdl.addCmdTerm(); //finally end your message with the term char

  // once the message is ready, send it
  // either by getting it and sending it however you want
  Serial.println(cmdHdl.getOutCmd()); // that will print the message on Serial
  // or by using the Serial using the directly embeded Serial send
  cmdHdl.sendCmdSerial(); // also send current Cmd to Serial (by default)
  // you can also set the default Out Serial to use by:
  // cmdHdl.setOutCmdSerial(Serial); // default is Serial
  Serial.println(); // just adding this so the ouput on the serial terminal looks nice

}



void loop() {
  cmdHdl.processSerial(Serial3);     
}
