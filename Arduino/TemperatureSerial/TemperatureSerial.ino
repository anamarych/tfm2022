#include <Wire.h>

byte lowByte, highByte;
int pinTemp = A1;
int led = 9;

const size_t dataLength = 32;
byte data[dataLength];

void setup() {
  Serial.begin(9600);
  Wire.begin();
  pinMode(led, OUTPUT);
}

void datos(int nSensors) {
  data[0] = 0;//Trama medidas de los sensores
  data[1] = 1;//Regleta I
  data[2] = 1;//Tipo mota sensora
  data[3] = 3;//Mota III
  data[4] = nSensors;//1 Sensor
}

void loop() {
  int temp = analogRead(pinTemp);
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println("C");
  
  Serial.println("cut value to 8 first bits and 8 last bits");
  lowByte  = (temp & 0xff);
  highByte = ((temp >> 8) & 0xff);
  Serial.println(highByte,BIN);
  Serial.println(lowByte,BIN);
  
  Serial.println("get back the initial read value");
  int A3ValueReceived = ((int)highByte  << 8) + lowByte;
  Serial.println(A3ValueReceived);
  delay(1000);  
}
