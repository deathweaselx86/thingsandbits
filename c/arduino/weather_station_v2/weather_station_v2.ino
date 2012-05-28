/*

This is an IEEE 802.15.4 based weather monitor sketch.
It's really just half of the solution; the other half will be
a Processing sketch that will intercept the messages and
send them to Cosm.

Jessica Ross
deathweasel@gmail.com

Thank you to ladyada, nethoncho et al for the DHT22 
code!
*/

#include <DHT.h>
#include <XBee.h>

#define DHTTYPE DHT22

// Sensor information.
// DHT22 sensor is set up on digital pin 7.
const int DHTPIN=7;
DHT dht(DHTPIN, DHTTYPE);

// XBee information.
// Allocate 4 bytes of data for each sensor value passed.
byte payload[] = {0,0,0,0,0,0,0,0};
XBee xbee = XBee();
TxStatusResponse txStatus = TxStatusResponse();
Tx16Request tx16 = Tx16Request(0x6142, payload, sizeof(payload));


float humidity, temp;
String data;

void setup()
{
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  xbee.begin(19200);
  dht.begin();
  delay(5000);

}

void loop()
{
    temp = dht.readTemperature();
    humidity = dht.readHumidity();
    sendData(temp,humidity);
    delay(2000);
}

void sendData(float temp, float humidity)
{
    // Trick compiler into letting us bit shift float
    // by pointing to it with an integer pointer. I hate
    // this so much and yet I can't accomplish what I want
    // without it.
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
    delay(5000);
    for(int i=0;i<sizeof(payload); i++)
      payload[i] = 0;
    int * tempPtr = (int *) (& temp);
    int * humidityPtr = (int *) (& humidity);
    //pack temp
    payload[0] = (*tempPtr >> 24) & 0xff;
    payload[1] = (*tempPtr >> 16) & 0xff;
    payload[2] = (*tempPtr >> 8) & 0xff;
    payload[3] = (*tempPtr) & 0xff;
    //pack humidity
    payload[4] = (*humidityPtr >> 24) & 0xff;
    payload[5] = (*humidityPtr >> 16) & 0xff;
    payload[6] = (*humidityPtr >> 8) & 0xff;
    payload[7] = (*humidityPtr) & 0xff;
    
    xbee.send(tx16);
    digitalWrite(9,HIGH);
    
    // Wait for the other XBee to let us know it got something.
    if (xbee.readPacket(5000)) {
        if (xbee.getResponse().getApiId() == TX_STATUS_RESPONSE) {
           xbee.getResponse().getZBTxStatusResponse(txStatus);
           if (txStatus.getStatus() == SUCCESS) {
               // Great. What should we do to denote success?
               digitalWrite(8,HIGH); 
                
           } else {
                // the other XBee did not receive our packet. What do
                // we do to denote failute?
                ;
                          }
        }      
    } else {
      // Did we miss the status response???
      ;
    }
}
