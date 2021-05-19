/***
 * Simple program for reporting the accelerometer X, Y, and Z axis values.
 * Based upon the MMA8452Q Example program from SparkFun by Jim Lindblom
 * 
 * Rev 1 - Jason Forsyth - 2/17/19
 * Rev 1.01 - modified to access Accel X, Y, Z directly. Avoids issues using the original (modified by JF) library
 */

//include Wire Library to access i2c
#include <Wire.h>

//include the MMA8452 library
#include <SparkFun_MMA8452Q.h>

//create a handle to the accelerometer
MMA8452Q accel;


void setup() {
  Serial.begin(9600);

  Serial.println("Hello World! Welcome to the Accel program!");

  /**
   * Initialize the accelerometer to +/- 2g and 800 Hz output
   * Parameters can be changed via library
   */
  accel.init();

}

void loop() {

  //direct access is bad but that's how the library is written.
  accel.read();
  
  float xAccel = accel.cx;

  float yAccel = accel.cy;

  float zAccel = accel.cz;

  Serial.print("X: ");
  Serial.print(xAccel,3); //print to three decimal places

  Serial.print(" Y: ");
  Serial.print(yAccel,3); //print to three decimal places

  Serial.print(" Z: ");
  Serial.println(zAccel,3); //print to three decimal places

  //delay 20ms for a 50Hz sample rate
  delay(20);

}
