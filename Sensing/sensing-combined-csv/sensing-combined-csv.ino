/**
   Combining basic examples from the CCS and BME boards by
   Nathan Seidle and Marshall Taylor into a single file.
   Code is based upon SparkFun examples and is
   not my own. See CCS and BME libraries for original source.

   Rev 1. - Jason Forsyth 2/6/19
*/

//include the Wire library to access the i2c interface
#include <Wire.h>

//include the libraries for the BME (humdity, pressure, altitude, and temperature)
//and the CCS (CO2 and TVOC) sensors
#include "SparkFunCCS811.h"
#include "SparkFunBME280.h"
#include <SparkFun_MMA8452Q.h>

//define the default I2C address of the CCS. Is not needed for BME
//as is already in library
#define CCS811_ADDR 0x5B //Default I2C Address

//create handles to the three sensors
BME280 bmeSensor;
CCS811 ccsSensor(CCS811_ADDR);
MMA8452Q accel;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  Wire.begin();

  /**
     Initial Environmental Combo Board
  */

  if (bmeSensor.beginI2C() == false) //Begin communication over I2C
  {
    Serial.println("Could not access the BME sensor. Please check wiring.");
    while (1); //Freeze
  }


  CCS811Core::status returnCode = ccsSensor.begin();
  if (returnCode != CCS811Core::SENSOR_SUCCESS)
  {
    Serial.println("Could not access the CCS sensor. Please check wiring.");
    while (1); //Hang if there was a problem.
  }

  /**
     Initial Accelerometer Board
  */

  /**
    Initialize the accelerometer to +/- 2g and 800 Hz output
    Parameters can be changed via library
  */
  accel.init();

}

void loop() {
  /**
   * Collect data from the Environmental Combo Board
   */

  ////////////////////// Get Data from the BME Board //////////////////////
  float humidity = bmeSensor.readFloatHumidity();
  float pressure = bmeSensor.readFloatPressure();
  float altitude = bmeSensor.readFloatAltitudeFeet();
  float temp = bmeSensor.readTempF();

  Serial.print(humidity, 0); //print with no decimal places

  Serial.print(",");
  Serial.print(pressure, 0); //print with no decimal places

  Serial.print(",");
  Serial.print(altitude, 1); //print with one decimal place

  Serial.print(",");
  Serial.print(temp, 2); // print with two decimal places

  ////////////////////// Get Data from the CCS Board //////////////////////

  //create init variables for CO2 and TVOC. Give them some initial value
  //so we can know if they are not "fresh" data from the sensor.
  int CO2 = -1;
  int TVOC = -1;

  //check to see if CCS sensor is ready
  if (ccsSensor.dataAvailable())
  {
    //If so, have the sensor read and calculate the results.
    ccsSensor.readAlgorithmResults();

    //request data from the sensor
    CO2 = ccsSensor.getCO2();
    TVOC = ccsSensor.getTVOC();
  }

  Serial.print(",");
  Serial.print(CO2);  //don't have to deal with decimals are result is integer

  Serial.print(",");
  Serial.print(TVOC); //don't have to deal with decimals are result is integer

  /**
   * Collect data from the accelerometer
   */

   //direct access is bad but that's how the library is written.
  accel.read();
  
  float xAccel = accel.cx;

  float yAccel = accel.cy;

  float zAccel = accel.cz;

  Serial.print(",");
  Serial.print(xAccel,3); //print to three decimal places

  Serial.print(",");
  Serial.print(yAccel,3); //print to three decimal places

  Serial.print(",");
  Serial.print(zAccel,3); //print to three decimal places

////////////////////// Print Out the Time //////////////////////
  //get the number of milliseconds since the processor was turned on
  long runTime = millis();

  Serial.print(",");
  Serial.println(runTime); //print out the time as a new line to end this line


  //take a 1000ms break. Don't overwhelm the bus and print screen
  //You can "go faster" but the CCS sensor won't be ready except every 1s (approx.)
  //Accel can go much faster
  delay(500);

}
