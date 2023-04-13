#include <Servo.h>

class RobotControl {
  private:
    Servo S1;
    String entradaSerial = ""; 
    bool entradaCompleta = false;

  public:
    RobotControl(int pin_S  ) {
      S1.attach(pin_S);
      S1.write(0);
      delay(1000);
    }

    void start() {
      if (entradaCompleta) {
        if (entradaSerial == "b'izq1\n'") {
          S1.write(0);
          delay(10);
        } else if (entradaSerial == "izq2\n") {
          S1.write(30);
          delay(10); 
        } else if (entradaSerial == "izq3\n") {
          S1.write(60);
          delay(10); 
        } else if (entradaSerial == "ctr\n") {
          S1.write(90);
          delay(10);
        } else if (entradaSerial == "der1\n") {
          S1.write(120);
          delay(10);
        } else if (entradaSerial == "der2\n") {
          S1.write(150); 
          delay(10);
        } else if (entradaSerial == "der3\n") {
          S1.write(180); 
          delay(10);
        }
        entradaSerial = ""; 
        entradaCompleta = false; 
      }
    }

    void handleSerialEvent() {
      if (Serial.available() > 0) {
        char inChar = (char)Serial.read();
        entradaSerial += inChar; 
        Serial.write(inChar);
        delay(10);
        if (inChar == '\n') {
          entradaCompleta = true;
        }
      }
    }
};

RobotControl robot(10);

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
}

void loop() {
  robot.handleSerialEvent();
  robot.start();
}
