#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//Add the Si4735 Library to the sketch.
#include <Si4735.h>

//Create an instance of the Si4735 classes
Si4735 radio;
Si4735RDSDecoder decoder;
char command;
byte mode, status;
word frequency, rdsblock[4];
bool goodtune;
Si4735_RX_Metrics RSQ;
Si4735_RDS_Data station;
Si4735_RDS_Time rdstime;
char FW[3], REV, buffer[64];
word myFrequency = 88.5;

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);



void setup()
{
  Serial.begin(9600);
  
  radio.begin(SI4735_MODE_FM);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3D);  
  
}


void refreshDisplay()
{
  display.clearDisplay();
  display.setCursor(10,0);
  display.setTextSize(0);
  display.setTextColor(WHITE);
  radio.seekDown();
  radio.sendCommand(SI4735_CMD_GET_INT_STATUS);
  if(radio.readRDSBlock(rdsblock)) 
         decoder.decodeRDSBlock(rdsblock);
  
  String frequencyString;
  frequency = radio.getFrequency();
  frequencyString = String(frequency/100) + "." + String(frequency % 100) + String(" Mhz");
  //display.setCursor(0,0);
  frequencyString.toCharArray(buffer,64);
  display.println(buffer);
  if(radio.isRDSCapable())
  {
     decoder.getRDSData(&station);
     display.println(station.programService);
     display.println(station.programTypeName);
     display.println(station.radioText); 
  }
  display.display();
}  


void loop()
{
  if (millis() % 5000 == 0)
    refreshDisplay();
}

