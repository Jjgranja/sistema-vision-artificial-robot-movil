#include <Servo.h>

Servo motor1, motor2, motor3, motor4;

#define MOTOR_PIN1 9
#define MOTOR_PIN2 10
#define MOTOR_PIN3 11
#define MOTOR_PIN4 12

#define ENCODER1_PIN 2
#define ENCODER2_PIN 3
#define ENCODER3_PIN 21
#define ENCODER4_PIN 20

volatile int pulseCount1 = 0;
volatile int pulseCount2 = 0;
volatile int pulseCount3 = 0;
volatile int pulseCount4 = 0;

unsigned long lastTime = 0;
float rpm_right = 0;
float rpm_left = 0;

char ultimoComandoManual = 'x';

void countPulse1() { pulseCount1++; }
void countPulse2() { pulseCount2++; }
void countPulse3() { pulseCount3++; }
void countPulse4() { pulseCount4++; }

void detener() {
  motor1.write(90);
  motor2.write(90);
  motor3.write(90);
  motor4.write(90);
}

void avanzar() {
  motor1.write(160);
  motor2.write(160);
  motor3.write(160);
  motor4.write(160);
}

void retroceder() {
  motor1.write(20);
  motor2.write(20);
  motor3.write(20);
  motor4.write(20);
}

void girarDerecha() {
  motor1.write(100);
  motor2.write(100);
  motor3.write(160);
  motor4.write(160);
}

void girarIzquierda() {
  motor1.write(160);
  motor2.write(160);
  motor3.write(100);
  motor4.write(100);
}

void ejecutarManual(char command) {
  switch (command) {
    case 'w': avanzar(); break;
    case 's': retroceder(); break;
    case 'x': detener(); break;
    case 'd': girarDerecha(); break;
    case 'a': girarIzquierda(); break;

    case 'c':
      motor1.write(80); motor2.write(80);
      motor3.write(20); motor4.write(20);
      break;

    case 'z':
      motor1.write(20); motor2.write(20);
      motor3.write(80); motor4.write(80);
      break;

    case 'q':
      motor1.write(160); motor2.write(160);
      motor3.write(20); motor4.write(20);
      break;

    case 'e':
      motor1.write(20); motor2.write(20);
      motor3.write(160); motor4.write(160);
      break;
  }
}

void ejecutarVision(char command) {
  switch (command) {
    case 'X': detener(); break;
    case 'D': girarDerecha(); break;
    case 'A': girarIzquierda(); break;

    // SEGURO y ALERTA no reemplazan el mando manual.
    case 'O':
    case 'L':
      ejecutarManual(ultimoComandoManual);
      break;
  }
}

void calculateRPM() {
  unsigned long currentTime = millis();

  if (currentTime - lastTime >= 2000) {
    float rpm_motor1 = (pulseCount1 / 20.0) * 30.0;
    float rpm_motor2 = (pulseCount2 / 20.0) * 30.0;
    float rpm_motor3 = (pulseCount3 / 20.0) * 30.0;
    float rpm_motor4 = (pulseCount4 / 20.0) * 30.0;

    rpm_right = (rpm_motor1 + rpm_motor3) / 2.0;
    rpm_left = (rpm_motor2 + rpm_motor4) / 2.0;

    pulseCount1 = 0;
    pulseCount2 = 0;
    pulseCount3 = 0;
    pulseCount4 = 0;
    lastTime = currentTime;

    Serial.print(rpm_right);
    Serial.print(',');
    Serial.println(rpm_left);
  }
}

void setup() {
  motor1.attach(MOTOR_PIN1);
  motor2.attach(MOTOR_PIN2);
  motor3.attach(MOTOR_PIN3);
  motor4.attach(MOTOR_PIN4);

  Serial.begin(9600);   // USB Jetson <-> Arduino
  Serial1.begin(9600);  // Bluetooth / APK

  pinMode(ENCODER1_PIN, INPUT_PULLUP);
  pinMode(ENCODER2_PIN, INPUT_PULLUP);
  pinMode(ENCODER3_PIN, INPUT_PULLUP);
  pinMode(ENCODER4_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCODER1_PIN), countPulse1, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER2_PIN), countPulse2, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER3_PIN), countPulse3, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER4_PIN), countPulse4, RISING);

  detener();
}

void loop() {
  // Control manual existente desde la APK/Bluetooth.
  if (Serial1.available() > 0) {
    ultimoComandoManual = Serial1.read();
    ejecutarManual(ultimoComandoManual);
  }

  // Capa visual proveniente de puente_arduino.py.
  if (Serial.available() > 0) {
    char commandVision = Serial.read();
    ejecutarVision(commandVision);
  }

  calculateRPM();
}
