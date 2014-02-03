/****
  This sketch runs a munny clock.
****/

#include <Wire.h>
#include "RTClib.h"
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>

RTC_DS1307 RTC;
Adafruit_7segment matrix = Adafruit_7segment();

void setup() {
  
    Wire.begin();
    RTC.begin();
    matrix.begin(0x70);

    // Set up Timer1 so we can just check the time once per
    // second instead of just waiting. The maximum wait time 
    // I'm allowed to use is a bit more than 4s, but this is good enough.
    cli();
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;
    // Turn on CTC mode; count up to 15624 before 
    // triggering interrupt.
    TCCR1B |= (1 <<WGM12);
    OCR1A = 15624; 
    TCCR1B = (1 << CS10) | (1 << CS12);
    TIMSK1 = (1 << OCIE1A); 
    sei();  
}

void loop()
{
    set_sleep_mode(SLEEP_MODE_IDLE);
    sleep_enable();
    sleep_mode();
    sleep_disable();
}
  
ISR(TIMER1_COMPA_vect)
{
  // This is quite redundant. I don't feel comfortable updating only when
  // now.second() returns 0. Maybe add an extra two segments to the display to
  // show seconds?
  int hours, minutes;
  DateTime now = RTC.now();
  
  
  // Read RTC and write matrix display
  hours = now.hour();
  minutes = now.minute();
  
  matrix.writeDigitNum(0,hours/10, true);
  matrix.writeDigitNum(1, hours % 10, true);
  matrix.drawColon(true);
  matrix.writeDigitNum(3, minutes/10, false);
  matrix.writeDigitNum(4, minutes%10, false);
  matrix.writeDisplay();
    
}
