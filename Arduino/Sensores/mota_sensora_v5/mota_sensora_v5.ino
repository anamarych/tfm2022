//motas 65793, 65795, 131332, 131334 
//DH:13A200
//DL:418996C5

//Librerías necesarias
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

#define DHTPIN 2
#define DHTTYPE DHT22

BH1750 lightMeter;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
DHT dht(DHTPIN, DHTTYPE);
int led = 13;

const size_t dataLength = 32;
byte data[dataLength];

void setup() {
  Serial.begin(9600);
  Wire.begin();
  dht.begin();
  lightMeter.begin();
  mlx.begin();
  pinMode(led, OUTPUT);
}

void datos(int nSensors) {
  data[0] = 0;//Trama medidas de los sensores
  data[1] = 2;//Regleta
  data[2] = 1;//Tipo mota sensora
  data[3] = 5;//Mota
  data[4] = nSensors;//5 Sensores(Son 3 pero toman mas de una medida)
}

void humedad() {
  float h = dht.readHumidity(); //Se lee la humedad
  float t = dht.readTemperature(); //Se lee la temperatura
  typedef union {
    float number;
    byte bytes[4];
  } FLOATUNION_t;
  
  FLOATUNION_t humedad,temperatura;
  humedad.number = h;
  temperatura.number = t;
  
  data[5] = 1;//Identificador sensor "Humedad relativa"
  int a;
  for (int i = 6; i < 10; i++)
  {
    data[i] = humedad.bytes[a];
    a++;
  }
  data[10] = 0;//Identificador sensor "Temperatura ambiente"
  a=0;
  for (int i = 11; i < 15; i++)
  {
    data[i] = temperatura.bytes[a];
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
  
  data[15] = 2;//Identificador sensor "Intensidad lumínica"
  int a;
  for (int i = 16; i < 20; i++)
  {
    data[i] = luminosidad.bytes[a];
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

  FLOATUNION_t ambiente,superficie;
  ambiente.number = amb;
  superficie.number = sup;

  data[20] = 10;//Identificador sensor "Temperatura ambiente"
  int a;
  for (int i = 21; i < 25; i++)
  {
    data[i] = ambiente.bytes[a];
    a++;
  }

  data[25] = 4;//Identificador sensor "Temperatura superficie"
  a=0;
  for (int i = 26; i < 30; i++)
  {
    data[i] = superficie.bytes[a];
    a++;
  }
}

void loop() {
  //Definimos el tiempo de muestreo
  //delay(900000);
  datos(5);//Número de sensores
  lux();
  temperatura();
  humedad();
  data[sizeof(data) - 2] = 13;//Retorno de carro
  data[sizeof(data) - 1] = 10;//Salto de línea
  Serial.write(data, sizeof(data));
  digitalWrite(led, HIGH); //Activa led
  delay(2000); //Retardo
  digitalWrite(led, LOW); //Apaga led
  delay(2000);
}
