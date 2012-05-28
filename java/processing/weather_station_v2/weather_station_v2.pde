import processing.serial.*;

XBee xbee;
  
void setup() {
  try { 

    xbee = new XBee();
    // replace with your COM port
    xbee.open("/dev/tty.usbserial-AH01D7MI", 19200);
    System.out.println("Initializing XBee.");
    System.out.println(xbee.toString());
    System.out.println(xbee.isConnected());
    delay(5000);

    } 
  catch (Exception e) {
    System.out.println("XBee failed to initialize");
    e.printStackTrace();
    System.exit(1);
  }
}

void draw() {
  try {
      int [] data = new int[2];
      
      while (true)
      {
          System.out.println("Listening for messages.");
          
          XBeeResponse response = xbee.getResponse();
          System.out.println("Got response.");
          RxResponse16 rx16 = (RxResponse16) response;
          
          data = rx16.getData();
          System.out.println(float(data[0]));
          delay(2000);
      }
  
  } 
  catch (Exception e) {
    e.printStackTrace();
  }
}
