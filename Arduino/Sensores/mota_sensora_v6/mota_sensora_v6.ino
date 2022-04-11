// mota 65799

#include <Wire.h>
#include "SparkFun_SCD30_Arduino_Library.h" 

SCD30 co2Sensor;
int analogPin = A0;
int val = 0; 
int totalN=0;
int count=0;
int wait=0;
int umbralN=10;

const int button =2;

byte dataCo2Sensor[22];
byte dataNoise[12];

void setup() {
  Wire.begin();
  Serial.begin(9600);
  co2Sensor.begin();
  co2Sensor.setMeasurementInterval(100);
  ///Madrid altitude over the sea level
  co2Sensor.setAltitudeCompensation(667);

  //add end frame  
  dataCo2Sensor[sizeof(dataCo2Sensor) - 2] = 13;
  dataCo2Sensor[sizeof(dataCo2Sensor) - 1] = 10;

  dataNoise[sizeof(dataNoise) - 2] = 13;
  dataNoise[sizeof(dataNoise) - 1] = 10;
  pinMode(button, INPUT);
}

void addHeader(int nSensors, byte *data) {
  data[0] = 0;//Trama medidas de los sensores
  data[1] = 1;//Regleta
  data[2] = 1;//Tipo mota sensora
  data[3] = 7;//
  data[4] = nSensors;//
}

void readCO2Sensor(){      
typedef union {
  float number;
  byte bytes[4];
} FLOATUNION_t;

  float c, h, t;
  FLOATUNION_t co2, temperature, humidity; 
  
  if(co2Sensor.dataAvailable()){
      c= co2Sensor.getCO2();
      t=co2Sensor.getTemperature();
      h=co2Sensor.getHumidity();

      co2.number=c;
      temperature.number=t;
      humidity.number=h;
      
      addHeader(3, dataCo2Sensor);

      ////humidity
      int a=0; 
      dataCo2Sensor[5]=1;
      for(int i=6; i<10; i++){
        dataCo2Sensor[i]=humidity.bytes[a];
        a++;
      }

      ///enviromental temperature
      dataCo2Sensor[10]=0;
      a=0;
      for(int i=11; i<15; i++){
        dataCo2Sensor[i]=temperature.bytes[a];
        a++;
      }

      ///co2
      dataCo2Sensor[15]=3;
      a=0;
      for(int i=16; i<20; i++){
        dataCo2Sensor[i]=co2.bytes[a];
        a++;
      }
       Serial.write(dataCo2Sensor, sizeof(dataCo2Sensor)); 
    }  
 }

void readNoise(){ 
  typedef union {
  float number;
  byte bytes[4];
} FLOATUNION_t;
  float valN=0;
  FLOATUNION_t noise;
  
  val = analogRead(analogPin); 
  totalN=totalN+val;
  count++;
  if(count==10){
    valN=totalN/count;
    if(valN>=umbralN){
        addHeader(1, dataNoise);
        noise.number=valN;
        int a=0;
        dataNoise[5]=11;
        for(int i=6; i<10; i++){
          dataNoise[i]=noise.bytes[a];
          a++;
        }
        Serial.write(dataNoise, sizeof(dataNoise));        
        wait=600;
      }    
    count=0;
    totalN=0;  
  } 
  delay(10);
}
 

void loop() {
      
    readCO2Sensor();
    if(wait==0){
      readNoise();
     }else{
      delay(100);
      wait--;
     }
}
