#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo gripper;

void setup() {
  base.attach(A1);
  shoulder.attach(A2);
  elbow.attach(A3);
  gripper.attach(A0);

  Serial.begin(9600);
  Serial.println("Send number (0–6) to move to that position");
}

// ---------- Position Functions ----------
void pos0() {
  base.write(100);
  elbow.write(170);
  shoulder.write(70);
  delay(2000);
  gripper.write(100);

}

void pos1() {
  base.write(100);
  elbow.write(170);
  shoulder.write(70);
  delay(2000);
  gripper.write(100);
}

void pos2() {  
  base.write(57);
  delay(2000);
  shoulder.write(130);
  delay(2000);
  elbow.write(120);
  delay(2000);
  gripper.write(55);
  delay(2000);
}

void pos3() {
  base.write(50);
  delay(2000);
  shoulder.write(130);
  delay(2000);
  elbow.write(130);
  delay(2000);
  gripper.write(55);
  delay(2000);
}
void pos4() {
  base.write(38);
  delay(2000);
  shoulder.write(130);
  delay(2000);
  elbow.write(130);
  delay(2000);
  gripper.write(55);
  delay(2000);
}

void pos5() {
  base.write(20);
  delay(2000);
  shoulder.write(130);
  delay(2000);
  elbow.write(130);
  delay(2000);
  gripper.write(55);
  delay(2000);
}

void pos6() {
  base.write(10);
  delay(2000);
  elbow.write(120);
  delay(2000);
  shoulder.write(130);
  delay(2000);
  gripper.write(55);
  delay(2000);
 
}


void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    switch (cmd) {
      case '0': pos0(); break;
      case '1': pos1(); break;
      case '2': pos2(); break;
      case '3': pos3(); break;
      case '4': pos4(); break;
      case '5': pos5(); break;
      case '6': pos6(); break;
      

      default: Serial.println("Invalid command"); break;
    }

    Serial.print("Moved to position ");
    Serial.println(cmd);
  }
}
