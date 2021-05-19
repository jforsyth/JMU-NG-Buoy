// Feather9x_TX
// -*- mode: C++ -*-
// Example sketch showing how to create a simple messaging client (transmitter)
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example Feather9x_RX

#include <SPI.h>
#include <RH_RF95.h>

//for feather32u4
//  #define RFM95_CS 8
//  #define RFM95_RST 4
//  #define RFM95_INT 7

// for feather m0
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3



/* for shield
  #define RFM95_CS 10
  #define RFM95_RST 9
  #define RFM95_INT 7
*/

/* Feather 32u4 w/wing
  #define RFM95_RST     11   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     2    // "SDA" (only SDA/SCL/RX/TX have IRQ!)
*/

/* Feather m0 w/wing
  #define RFM95_RST     11   // "A"
  #define RFM95_CS      10   // "B"
  #define RFM95_INT     6    // "D"
*/

#if defined(ESP8266)
/* for ESP w/featherwing */
#define RFM95_CS  2    // "E"
#define RFM95_RST 16   // "D"
#define RFM95_INT 15   // "B"

#elif defined(ESP32)
/* ESP32 feather w/wing */
#define RFM95_RST     27   // "A"
#define RFM95_CS      33   // "B"
#define RFM95_INT     12   //  next to A

#elif defined(NRF52)
/* nRF52832 feather w/wing */
#define RFM95_RST     7   // "A"
#define RFM95_CS      11   // "B"
#define RFM95_INT     31   // "C"

#elif defined(TEENSYDUINO)
/* Teensy 3.x w/wing */
#define RFM95_RST     9   // "A"
#define RFM95_CS      10   // "B"
#define RFM95_INT     4    // "C"
#endif

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 434.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup()
{
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(9600);
  while (!Serial) {
    delay(1);
  }

  delay(100);

  Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);


  //test if RF95 chip has been initialized correctly
  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

//this is the maximum length of bytes we can transmit. Internally, the
//RF95 chip has 251 bytes. Lets not get near that limit.
//https://github.com/adafruit/RadioHead/blob/master/RH_RF95.h
const int BUFFER_LENGTH = 128;

//give radiopacket a better name. It's really a transmit buffer
char tx_buffer[BUFFER_LENGTH];


//create a new message buffer. This time, of maximum length supported by the radio
uint8_t rx_buffer[BUFFER_LENGTH];

void loop()
{
  delay(1000); // Wait 1 second between transmits, could also 'sleep' here!
  Serial.println("Transmitting..."); // Send a message to rf95_server

  /*
  * *****************************BEGIN Dr. Forsyth Custom Code *****************************
  */

  //clear buffer by setting all values to 0
  memset(tx_buffer, 0, BUFFER_LENGTH);

  //terminate string
  tx_buffer[BUFFER_LENGTH - 1] = 0;

  //check to see if any data is in the serial port
  if (Serial.available() > 0)
  {
    //read all data from the Serial port until its empty or the buffer is full
    for (int i = 0; Serial.available() > 0 && i < BUFFER_LENGTH - 1; i++)
    {
      tx_buffer[i] = Serial.read();
    }

    //clear out the serial port of any remaining data. We're just going
    //to drop it ....
    while (Serial.available() > 0) {
      char c = Serial.read();
    }
  }
  else //copy in the dummy string
  {
    //copy dummy string into receive buffer
    String string_to_send = "Hello world!";
    string_to_send.getBytes((unsigned char*)tx_buffer, BUFFER_LENGTH);
  }

  /*
  * *****************************END Dr. Forsyth Custom Code *****************************
  */


  //prepare radiopacket for transmission...

  //print a helpful(?) message
  Serial.print("Sending "); Serial.println(tx_buffer);

  //ensure radiopacket is null-terminated
  tx_buffer[BUFFER_LENGTH - 1] = 0;

  //print another helpful(?) message
  Serial.println("Sending...");
  delay(10);

  //actually send the message. Specifies the buffer that holds the information
  //and the length of that buffer
  rf95.send((uint8_t *)tx_buffer, BUFFER_LENGTH);

  //again, another helpful(?) message
  Serial.println("Waiting for packet to complete...");
  delay(10);

  //wait until packet is sent out of radio
  rf95.waitPacketSent();

  // Now wait for a reply

 

  //check how long that new buffer is
  uint8_t len = BUFFER_LENGTH;

  //Keep being verbose
  Serial.println("Waiting for reply...");

  //wait 1000ms for a message, if time out, then go to ELSE block
  if (rf95.waitAvailableTimeout(1000))
  {
    //read the message from the radio into the rx_buffer
    if (rf95.recv(rx_buffer, &len))
    {
      Serial.print("Got reply: ");
      Serial.println((char*)rx_buffer);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
  else
  {
    Serial.println("No reply, is there a listener around?");
  }

}
