/*

This is an IEEE 802.15.4 based weather monitor sketch.
It's really just half of the solution.

I decided to use another Arduino to send the data to Cosm
rather than spend the time to figure out how to cast a generic
bitstream to int in Processing. Lazy, sorry. I have other things
I want to do with the same time.

Jessica Ross
deathweasel@gmail.com

Thank you to ladyada, nethoncho et al for the DHT22 
code! Thanks to the xbee-arduino guys, too.

*/

#include <DHT.h>
#include <XBee.h>
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>

#define DHTTYPE DHT22

// Sensor information.
// DHT22 sensor is set up on digital pin 7.
const int DHTPIN=7;
DHT dht(DHTPIN, DHTTYPE);

// XBee information.
// Allocate 4 bytes of data for each sensor value passed.
byte payload[] = {0,0,0,0,0,0,0,0};
XBee xbee = XBee();
Tx16Request tx16 = Tx16Request(0x0, payload, sizeof(payload));


volatile float humidity, temp;

void setup()
{
 // XBee and sensor setup.
  xbee.begin(9600);
  dht.begin();
  pinMode(DHTPIN, INPUT);
  
  // Set up  Timer 1 for ISR that actually sends data so
  // we can maybe shut some things down for a few seconds
  // while we wait.
  cli(); // global interrupts off
  // TCCR1A and TCCR1B are reggisters that control Timer1
  // Set both to zero for bit operations.
  TCCR1A = 0;
  TCCR1B = 0; 
  
  TIMSK1 = (1 << TOIE1); // enable Timer1 overflow interrupt  
  // Set 1024 timer prescaler, which gets us something in 
  // the vicinity of 4 s. I wish we could get something longer
  // than this.
  // Ideal would be 10 s. 
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << CS12);
  sei(); // global interrupts on
}


void loop()
{
  
  // Set up sleep mode.
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  // Actually sleep.
  sleep_mode();
  // We continue here after the interrupt.
  // Sleep mode disabled in interrupt.

}

ISR(TIMER1_OVF_vect)
{
    // Turn things on!
    sleep_disable();
    temp = dht.readTemperature();
    humidity = dht.readHumidity();
    sendData(temp,humidity);
    // Shut things down!
}

void sendData(float temp, float humidity)
{
    // Trick compiler into letting us bit shift float
    // by pointing to it with an integer pointer. I hate
    // this so much and yet I can't accomplish what I want
    // without it.
    
    for(int i=0;i<sizeof(payload); i++)
      payload[i] = 0;
    int * tempPtr = (int *) (& temp);
    int * humidityPtr = (int *) (& humidity);
    //pack temp
    payload[0] = *tempPtr >> 24 & 0xff;
    payload[1] = *tempPtr >> 16 & 0xff;
    payload[2] = *tempPtr >> 8 & 0xff;
    payload[3] = *tempPtr & 0xff;
    //pack humidity
    payload[4] = *humidityPtr >> 24 & 0xff;
    payload[5] = *humidityPtr >> 16 & 0xff;
    payload[6] = *humidityPtr >> 8 & 0xff;
    payload[7] = *humidityPtr & 0xff;
   
    xbee.send(tx16);
    // I don't care about the other XBee's response, so
    // why bother?    
    
}
