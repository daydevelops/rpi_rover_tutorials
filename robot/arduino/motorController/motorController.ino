#include <string.h>
// motor 1
int enA = 10;
int in1 = 9; 
int in2 = 8;
// motor 2
int in3 = 7;
int in4 = 6;
int enB = 5;

String msg = "";
char command;
int msgReceived = 1;
void setup() {
  pinMode(enA,OUTPUT);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(enB,OUTPUT);
  Serial.begin(9600); // Starts the serial communication
}

void processMessage(char command, String msg) {
  switch (command) {
    case 'L':
      changeLeftMotor(atoi(msg.c_str()));
      break;
    case 'R':
      changeRightMotor(atoi(msg.c_str()));
      break;
    case 'S':
      stopMotors();
      break;
  } 
}

void changeLeftMotor(int speed) {
  if (speed<0) {
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    speed = speed*-1;
  } else {
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  analogWrite(enA,speed);
}

void changeRightMotor(int speed) {
  if (speed<0) {
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    speed = speed*-1;
  } else {
    digitalWrite(in3,LOW);
    digitalWrite(in4,HIGH);
  }
  analogWrite(enB,speed);
}

void stopMotors() {
  digitalWrite(in1,LOW);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
  analogWrite(enA,0);
  analogWrite(enB,0);
}

void loop() {
  
  char character; // incoming charcater

  while(Serial.available()) {
      character = Serial.read();
      
      // if this is the start of a new command
      if (msgReceived==1) {
        command = character; // first character is for command type
        msgReceived = 0;
        continue;
      }
      
      if (character == ';') { // end of command
        processMessage(command,msg);
        msg = "";
        msgReceived = 1; // reset
      } else { // character is not the beginning or end of msg
        msg.concat(character);
      }
  }
  
  delay(50);

}
