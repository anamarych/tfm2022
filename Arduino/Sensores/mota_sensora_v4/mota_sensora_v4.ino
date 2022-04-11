//motas 65794 y 131333
//Librerias necesarias
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#define DHTTYPE DHT22

const int LEDPin = 13;     //Pin donde está el led
const int DHTPin = 2;     //Pin al que está conectado el DHT22
const int analogPin = A3;

DHT dht(DHTPin, DHTTYPE); //Declaramos el Sensor DHT22
BH1750 lightMeter;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

const size_t dataLength = 37;


byte dataSensors[32];
byte dataMovement[12];
int count=0;


void setup() {
  Serial.begin(9600);
  Wire.begin();
  pinMode(LEDPin, OUTPUT);
  pinMode(analogPin, INPUT_PULLUP);
  dht.begin();
  lightMeter.begin();
  mlx.begin();

  ///asigno final de trama
  dataSensors[sizeof(dataSensors) - 2] = 13;
  dataSensors[sizeof(dataSensors) - 1] = 10;

  dataMovement[sizeof(dataMovement) - 2] = 13;//Retorno de carro
  dataMovement[sizeof(dataMovement) - 1] = 10;
}

void crearHeader(int nSensors, byte *data) {
  data[0] = 0;//Trama medidas de los sensores
  data[1] = 2;//Regleta
  data[2] = 1;//Tipo mota sensora
  data[3] = 5;//Mota II
  data[4] = nSensors;
}

void movimiento() {
  int value = analogRead(analogPin);    
  crearHeader(1, dataMovement);
  dataMovement[5] = 7; //Identificador sensor "Sensor Movimiento"
  if (value > 100) {
    dataMovement[6] = 0;
    dataMovement[7] = 0;
    dataMovement[8] = 0;
    dataMovement[9] = 1; //Se ha detectado movimiento 
    Serial.write(dataMovement, sizeof(dataMovement));
  } 
}


void humedad() {
  float h = dht.readHumidity(); //Se lee la humedad
  float t = dht.readTemperature(); //Se lee la temperatura
  typedef union {
    float number;
    byte bytes[4];
  } FLOATUNION_t;

  FLOATUNION_t humedad, temperatura;
  humedad.number = h;
  temperatura.number = t;

  dataSensors[5] = 1;//Identificador sensor "Humedad relativa"
  int a;
  for (int i = 6; i < 10; i++)
  {
    dataSensors[i] = humedad.bytes[a];
    a++;
  }
  dataSensors[10] = 0;//Identificador sensor "Temperatura ambiente"
  a = 0;
  for (int i = 11; i < 15; i++)
  {
    dataSensors[i] = temperatura.bytes[a];
    a++;
  }
}

void lux() {
  float lux = lightMeter.readLightLevel();
  typedef union {
    float number;
    byte bytes[4];
  } FLOATUNION_t;

  FLOATUNION_t luminosidad;
  luminosidad.number = lux;

  dataSensors[15] = 2;//Identificador sensor "Intensidad lumínica"
  int a;
  for (int i =16 ; i < 20; i++)
  {
    dataSensors[i] = luminosidad.bytes[a];
    a++;
  }
}

void temperatura() {
  float amb = mlx.readAmbientTempC();
  float sup = mlx.readObjectTempC();
  typedef union {
    float number;
    byte bytes[4];
  } FLOATUNION_t;

  FLOATUNION_t ambiente, superficie;
  ambiente.number = amb;
  superficie.number = sup;

  dataSensors[20] = 10;//Identificador sensor "Temperatura ambiente"
  int a;
  for (int i = 21; i < 25; i++)
  {
    dataSensors[i] = ambiente.bytes[a];
    a++;
  }

  dataSensors[25] = 4;//Identificador sensor "Temperatura superficie"
  a = 0;
  for (int i = 26; i < 30; i++)
  {
    dataSensors[i] = superficie.bytes[a];
    a++;
  }
}


void loop(){  
  movimiento();
//  if(count==450){
  delay(2000);
  crearHeader(5,dataSensors);
  humedad();
  lux();
  temperatura();    
  Serial.write(dataSensors, sizeof(dataSensors));
 //   count=0;
//    }
  delay(2000);  
  count++;
  }
