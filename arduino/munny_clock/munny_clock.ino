/****
  This sketch runs a munny clock.
****/

#include <Wire.h>
#include "RTClib.h"
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

RTC_DS1307 RTC;
Adafruit_7segment matrix = Adafruit_7segment();

void setup() {
  
    Wire.begin();
    RTC.begin();
    matrix.begin(0x70);
  }
  
void loop()
{
  int hours, minutes;
 
  // Our seven segment display only has a resolution of 1 minute,
  // so let's not update for a minute. 
  // TODO: Make this into an interrupt so I can save power.
  delay(100);
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
