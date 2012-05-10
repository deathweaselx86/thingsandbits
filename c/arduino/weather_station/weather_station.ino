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
const int postingInterval = 10000; // Send data every 10 seconds

// DHT22 sensor is set up on digital pin 7.
DHT22 DHT22pin(7);
EthernetClient client;
char server[] = "api.cosm.com";

// Expect "real" values between -99 and 99.99, plus a newline. Obviously
// values for temp less than -40 are errors and values less than 0 for humidity
// are errors.

float humidity, temp;
String data;

void setup()
{
  Serial.begin(9600);
  // If Ethernet fails, then don't bother with the contents of
  // the loop() function.
  if (Ethernet.begin(mac) == 0){
     Serial.println("Failed to get IP via DHCP");
     for(;;)
      ; 
  }
  delay(1000);
}

void loop()
{
    Serial.println("beginning of loop");
    DHT22_ERROR_t errorCode;
    delay(postingInterval);
    Serial.println("after delay");
    errorCode = DHT22pin.readData();
    Serial.println("after reading sensor");
    // These values are both out of sensor range.
    // I'll use these to log an error condition for now.
    temp = -99.0;
    humidity = -99.0;
  
    switch(errorCode)
    {
      case DHT_ERROR_NONE:
        temp = DHT22pin.getTemperatureC();
        humidity = DHT22pin.getHumidity();
        break;
       case DHT_ERROR_CHECKSUM:
        temp = DHT22pin.getTemperatureC();
        humidity = DHT22pin.getHumidity();
        Serial.print("check sum error ");
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
  
    data = constructCsvString(temp, humidity);
    Serial.println(data);
    sendData(data);
  
    Serial.print("Last time connection was made or attempted: ");
    Serial.println(lastConnectionTime);
 
}
 
 String constructCsvString(float temp, float humidity)
 {
   char buf[7] = "      "; 
   String csvString, dummyString;
   
   // Constructing a CSV inside a String object to make this
   // "easier". For each sensor variable, print the sensor id,
   // then convert the sensor float variable to a string,
   // trim the extra characters from it, then put it together.
   
   csvString = String("temp,");
   dtostrf(temp,4,2,buf);
   dummyString = String(buf);
   dummyString.trim();
   csvString = csvString + dummyString;
   
   csvString = csvString + "\nhumidity,";
   dtostrf(humidity,4,2,buf);
   dummyString = String(buf);
   dummyString.trim();
   csvString = csvString + dummyString;
   
   return csvString;
 }
 
 void sendData(String csvString)
 {

     if (client.connect(server,80)) {
         Serial.println("Connecting to cosm");
         
         client.print("PUT /v2/feeds/");
         client.print(FEEDID);
         client.println(".csv HTTP/1.1");
         client.println("Host: api.cosm.com");
         client.print("X-ApiKey: ");
         client.println(PACHUBEKEY);
         client.print("User-Agent: ");
         client.println(USERAGENT);
         client.print("Content-Length: ");
         client.println(csvString.length()); 
         client.println("Content-Type: text/csv");
         client.println("Connection: close");
         

         client.println(csvString);
         client.stop();
     }
     else {
        Serial.println("Connection failed.");
        Serial.println("Disconnecting");
        client.stop();
     }
     lastConnectionTime = millis();
     
  }
  


