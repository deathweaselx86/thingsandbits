/*
This sketch belongs to the other half of an
IEEE 802.15.4-based weather monitor solution.
It sends data received 
*/

#include <Ethernet.h>
#include <SPI.h>
#include <stdio.h>
#include <XBee.h>

#define PACHUBEKEY "uEiSX0-LtHYwtDXVlDT0AgalaP2SAKx2MWtWVExvK0Uxcz0g"
#define USERAGENT "New Arduino Feed"
#define FEEDID "59148"


XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
// create reusable response objects for responses we expect to handle 
Rx16Response rx16 = Rx16Response();

uint8_t payload[] = {0,0,0,0,0,0,0,0};


byte mac[] = { 
  0x90, 0xA2, 0xDA, 0x00, 0xA2, 0x1F};
EthernetClient client;
char server[] = "api.cosm.com";

// Expect "real" values between -99 and 99.99, plus a newline. Obviously
// values for temp less than -40 are errors and values less than 0 for humidity
// are errors.

String data;

void setup()
{
  xbee.begin(9600);
  // If Ethernet fails, then don't bother with the contents of
  // the loop() function.
  if (Ethernet.begin(mac) == 0){
     for(;;)
      ; 
  }
  delay(1000);
}

void loop()
{  
    
    int temp, humidity;
    temp = 0;
    humidity = 0;
    
    if (xbee.readPacket(225000)) { // There is data.
          xbee.getResponse().getRx16Response(rx16);
           for(int i=0;i<8;i++)
             payload[i] = rx16.getData(i);
        
    
          //unpack temp
          temp =  temp | (payload[0] << 8);
          temp = temp | payload[1];

          //unpack humidity
          humidity = humidity | (payload[2] >> 8);
          humidity = humidity | payload[3];
     
          data = constructCsvString(float(temp)/10, float(humidity)/10);
          sendData(data);
    }
 
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
         if (client.connect(server, 80)) {
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
           client.println();

           client.println(csvString);
           client.stop();
         }
         
  }
  


