#include <Wire.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(8, 9);
byte lowByte, highByte;
int pinTemp = A1;
int led = 9;

const size_t dataLength = 32;
byte data[dataLength];

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
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

void temperatura() {
  float t = analogRead(pinTemp);
  typedef union {
    float number;
    byte bytes[4];
  } FLOATUNION_t;

  FLOATUNION_t tempe;
  tempe.number = t; 
  
  for (int i = 0; i < 4; i++)
  {
    Serial.write(tempe.bytes[i]);
    Serial.println(tempe.bytes[i],BIN);
  }
  
 // data[20] = 10;//Identificador sensor "Temperatura"
 // int a;
 // for (int i = 21; i < 25; i++)
//  {
 //   data[i] = tempe.bytes[a];
//    a++;
 // }
}

void loop() {
  datos(5);
  temperatura();
 // data[sizeof(data) - 2] = 13;//Retorno de carro
//  data[sizeof(data) - 1] = 10;//Salto de línea
//  Serial.write(data, sizeof(data));
//  digitalWrite(led, HIGH); //Activa led
//  delay(1000); //Retardo
  digitalWrite(led, LOW); //Apaga led

    if(Serial.available())
  {
    mySerial.write(Serial.read());
    
  } 
//  int temp = analogRead(pinTemp);
//  Serial.print("Temperature: ");
//  Serial.print(temp);
//  Serial.println("C");
  
//  Serial.println("cut value to 8 first bits and 8 last bits");
//  lowByte  = (temp & 0xff);
//  highByte = ((temp >> 8) & 0xff);
//  Serial.println(highByte,BIN);
//  Serial.println(lowByte,BIN);
  
//  Serial.println("get back the initial read value");
//  int A3ValueReceived = ((int)highByte  << 8) + lowByte;
//  Serial.println(A3ValueReceived);
  delay(1000);  
}
