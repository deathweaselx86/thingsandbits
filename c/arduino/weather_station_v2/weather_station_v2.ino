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
#include <SoftwareSerial.h>

#define DHTTYPE DHT22

// Sensor information.
// DHT22 sensor is set up on digital pin 7.
const int DHTPIN=7;
const int XBEE_SLEEP_PIN = 9;
const int LOG_TIME = 255;

DHT dht(DHTPIN, DHTTYPE);

// XBee information.
// Allocate 4 bytes of data for each sensor value passed.
byte payload[] = {0,0,0,0};
XBee xbee = XBee();
Tx16Request tx16 = Tx16Request(0x0, payload, sizeof(payload));


volatile float humidity, temp;
volatile int humidity_i, temp_i;
volatile int timer_variable = 0;


void setup()
{
 // XBee and sensor setup.
  xbee.begin(9600);
  dht.begin();
  
  pinMode(DHTPIN, INPUT);
  pinMode(XBEE_SLEEP_PIN, OUTPUT);
  // Initially, the XBee sleeps.
  digitalWrite(XBEE_SLEEP_PIN, HIGH); 
  // Set up  Timer 1 for ISR that actually sends data so
  // we can maybe shut some things down for a few seconds
  // while we wait.
  cli(); // global interrupts off
  // TCCR1A and TCCR1B are registers that control Timer1
  // Set both to zero for bit operations.
  TCCR1A = 0;
  TCCR1B = 0; 
  
  TIMSK1 = (1 << TOIE1); // enable Timer1 overflow interrupt  
  
  // Set 1024 timer prescaler, which gets us something in 
  // the vicinity of 4 s. I wish we could get something longer
  // than this.
  // Ideal would be 10 s. 
  TCCR1B |= (1 << CS10) | (1 << CS12);
  sei(); // global interrupts on
}


void loop()
{
  
  // Set up sleep mode.
  // We can only use SLEEP_MODE_IDLE with
  // Timer1. Use different source of 
  // interrupt next time. 
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  // Actually sleep.
  sleep_mode();
  // We continue here after the interrupt.
  sleep_disable();
}

ISR(TIMER1_OVF_vect)
{

    // We set this up such that the contents
    // of this if statement should execute every 15 minutes.
    timer_variable +=1;
    if (timer_variable == LOG_TIME)
    {
      digitalWrite(XBEE_SLEEP_PIN, LOW);
      delay(30); // Delay to let it wake up from advanced sleep.
      temp = dht.readTemperature();
      humidity = dht.readHumidity();
      temp_i = int(temp*10);
      humidity_i = int(humidity*10);
      sendData(temp_i,humidity_i);
      digitalWrite(XBEE_SLEEP_PIN, HIGH);
      timer_variable = 0;
    }
}

void sendData(int temp_i, int humidity_i )
{

    //pack temp
    payload[0] = temp_i >> 8 & 0xff;
    payload[1] = temp_i & 0xff;
    //pack humidity
    payload[2] = humidity_i >> 8 & 0xff;
    payload[3] = humidity_i & 0xff;
   
    xbee.send(tx16);
    // I don't care about the other XBee's response, so
    // why bother?
 
    
}
