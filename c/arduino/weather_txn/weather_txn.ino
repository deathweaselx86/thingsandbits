/*
This sketch belongs to the other half of an
IEEE 802.15.4-based weather monitor solution.
It sends data received 
*/

#include <Ethernet.h>
#include <SPI.h>
#include <stdio.h>

#define PACHUBEKEY "redacted"
#define USERAGENT "Deathweasel's Weather Station Feed"
#define FEEDID "58534"


long lastConnectionTime = 0;
const int postingInterval = 60000; // Send data every 10 seconds

// DHT22 sensor is set up on digital pin 7.

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
    delay(postingInterval);
    Serial.println("after delay");
    Serial.println("after reading sensor");
    // These values are both out of sensor range.
    // I'll use these to log an error condition for now.
 
    data = constructCsvString(temp, humidity);
    Serial.println(data);
    sendData(data);
 
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
         
         // I get a 401 Authentication 401 Unauthorized response without this
         // Something tells me that's an issue that Cosm needs to hammer out.
         client.println("Authorization: Basic ZGVhdGh3ZWFzZWw6bmFuZHk4OA=="); 
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
  


