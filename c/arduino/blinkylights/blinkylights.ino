/*
  Simple blinky lights sketch for my Arduino UNO.
*/

// Use digital pins 13-10.
const int LEDout[] = {10,11,12,13};
// We want to insert some interval in between
// lighting our LEDs without holding up our entire
// show. Use millis. This idea taken from a sample sketch
// by David A. Mellis.

long previousMillis = 0; // Stores value of last measured millis()
long interval = 400; // interval at which to blink
int ledState = LOW;

void setup()
{
  // Initialize digital pin outputs
  // These default to inputs so no need
  // to initialize them as such.
  
  pinMode(LEDout[0],  OUTPUT);
  pinMode(LEDout[1],  OUTPUT);
  pinMode(LEDout[2],  OUTPUT);
  pinMode(LEDout[3],  OUTPUT);
  
  // Chose random LEDs to start out lit so
  // this sketch is less boring.
  randomSeed(analogRead(0));
  for(int i=0;i<4;i++)
    digitalWrite(LEDout[i], random()%2);
}

void loop()
{

  // check to see if it's time to blink the LED; that is, if the 
  // difference between the current time and last time you blinked 
  // the LED is bigger than the interval at which you want to 
  // blink the LED.
  unsigned long currentMillis = millis();
 
  if(currentMillis - previousMillis > interval) {
    // save the last time you blinked the LED 
    previousMillis = currentMillis;   

    // set the LED with the ledState of the variable:
    for(int i=0; i<4; i++)
    {
      if (digitalRead(LEDout[i]) == HIGH)
        digitalWrite(LEDout[i],  LOW);
      else
        digitalWrite(LEDout[i], HIGH);
    }
  }
}
