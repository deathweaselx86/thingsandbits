/*
deathweasel@gmail.com
This is a web-based weather monitor sketch.
The idea is to check the weather locally every so often, then
send the data to my local webserver and post it.

For now this sends data to pachube.com.
I might have to pull data from pachube.com to place on
deathweasel.net.

*/

#include <DHT.h>
#include <Ethernet.h>
#include <SPI.h>
#include <stdio.h>

#define COSMKEY "redacted"
#define USERAGENT "New Arduino Feed"
#define FEEDID 59148
#define DHTPIN 7
#define DHTTYPE DHT22

byte mac[] = { 
  0x90, 0xA2, 0xDA, 0x00, 0xA2, 0x1F};

long lastConnectionTime = 0;
const int postingInterval = 2000; // Send data every 10 seconds

// DHT22 sensor is set up on digital pin 7.
DHT dht(DHTPIN, DHTTYPE);
EthernetClient client;
char server[] = "api.cosm.com";

float humidity, temp;
String data;

void setup()
{
  Serial.begin(9600);
  dht.begin();
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
    delay(postingInterval);
    Serial.println("after delay");
    temp = dht.readTemperature();
    humidity = dht.readHumidity();
  
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
         client.println(COSMKEY);
         client.print("User-Agent: ");
         client.println(USERAGENT);
         
         client.print("Content-Length: ");
         client.println(csvString.length()); 
         client.println("Accepts: text/csv");
         client.println("Content-Type: text/plain");
         client.println("Connection: close");
         client.println();
         client.println(csvString);
         client.println();
         while (client.available() > 0)
         {
           char c = client.read();
           Serial.print(c);     }
         Serial.println(); 
     }
     else
     {
        Serial.println("Connection failed.");
        Serial.println("Disconnecting");
        client.stop();
     }
     lastConnectionTime = millis();
     
  }
  


