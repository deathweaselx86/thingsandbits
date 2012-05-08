/*
deathweasel@gmail.com
This is a web-based weather monitor sketch.
The idea is to check the weather locally every so often, then
send the data to my local webserver and post it.

For now this sends data to pachube.com.
I might have to pull data from pachube.com to place on
deathweasel.net.

*/

#include <DHT22.h>
#include <Ethernet.h>
#include <SPI.h>
#include <stdio.h>

#define PACHUBEKEY "redacted"
#define USERAGENT "Deathweasel's Weather Station Feed"
#define FEEDID "58534"

byte mac[] = { 
  0x90, 0xA2, 0xDA, 0x00, 0xA2, 0x1F};

long lastConnectionTime = 0;
boolean lastConnected = false;
const int postingInterval = 10*1000*60; // ten minutes?

// DHT22 sensor is set up on digital pin 7.
DHT22 DHT22pin(7);
EthernetClient client;
char buf[7];
float data = 0;

void setup()
{
  Serial.begin(9600);
  // If Ethernet fails, then don't bother with the contents of
  // the loop() function.
  delay(600);
  if (Ethernet.begin(mac) == 0){
     Serial.println("Failed to get IP via DHCP");
     for(;;)
      ; 
  }
  
}

void loop()
{
  DHT22_ERROR_t errorCode;
  // We can only check this once every 2 seconds or so.
  delay(2000);
  errorCode = DHT22pin.readData();
  
  switch(errorCode)
  {
    case DHT_ERROR_NONE:
      data = DHT22pin.getTemperatureC();
      Serial.println(data);
      break;
     case DHT_ERROR_CHECKSUM:
      data = DHT22pin.getTemperatureC();
 
      Serial.print("check sum error ");
      Serial.println(data);
      break;
    case DHT_BUS_HUNG:
      Serial.println("BUS Hung");
      break;
    case DHT_ERROR_NOT_PRESENT:
      Serial.println("Not Present");
      break;
    case DHT_ERROR_ACK_TOO_LONG:
      Serial.println("ACK time out");
      break;
    case DHT_ERROR_SYNC_TIMEOUT:
      Serial.println("Sync Timeout ");
      break;
    case DHT_ERROR_DATA_TIMEOUT:
      Serial.println("Data Timeout ");
      break;
    case DHT_ERROR_TOOQUICK:
      Serial.println("Polled to quick ");
      break;
  }
  
  if (!client.connected() && lastConnected){
      Serial.println();
      Serial.println("Disconnecting.");
      client.stop();      
    }
  
  if (!client.connected() && (millis() - lastConnectionTime > postingInterval))
      sendData(data);
  
  lastConnected = client.connected();
  
 }
 
 void sendData(float data)
 {
     /*  
       Try to connect to www.pachube.com. If it 
     */
     if (client.connect("api.pachube.com",80)) {
         Serial.println("Connecting to pachube");
         client.print("PUT /v2/feeds/");
         client.print(FEEDID);
         client.println(" HTTP/1.1");
         client.println("Host: api.pachube.com");
         client.print("X-PachebeApiKey: ");
         client.println(PACHUBEKEY);
         client.print("User-Agent: ");
         client.println(USERAGENT);
         client.print("Content-Length: ");
         client.println(4+getLength(data), DEC);    
       
         client.println("Content-Type: text/csv");
         client.println("Connection: close");
         client.println();
         
         client.print("temp,");
         client.println(data);  
         Serial.println("Disconnecting from pachube.");
         client.stop();
     }
     else {
        Serial.println("Connection failed.");
        Serial.println("Disconnecting");
        client.stop();
     }
     lastConnectionTime = millis();
     
  }
  
// This method is copied from the PachubeClient example code. 
int getLength(int someValue) {
  // there's at least one byte:
  int digits = 1;
  // continually divide the value by ten, 
  // adding one to the digit count for each
  // time you divide, until you're at 0:
  int dividend = someValue /10;
  while (dividend > 0) {
    dividend = dividend /10;
    digits++;
  }
  // return the number of digits:
  return digits;
}
