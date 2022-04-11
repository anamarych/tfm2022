#include <SoftwareSerial.h>
SoftwareSerial mySerial(8, 9);
void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
} 
void loop()
{   
  if(Serial.available())
  {
    mySerial.write(Serial.read());
    
  } 
} 
