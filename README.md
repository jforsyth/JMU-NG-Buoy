# JMU_NG_Buoy
Code repository for JMU + NG Buoy designed by JMU Sophomore Engineers (Class of 2023)

**GPS/** Stand alone Python program to access Adafruit Ultimate GPS board via USB.

**LoRa/** Folder containing source code and libraries for AdaFruit Feather M0 LoRa radios. Currently setup to echo messages from TX to RX and return.

**Pi/** Python3 code for Raspbery Pi (version 4 prefered) to receive data from Arduino Sensing board and USB GPS. Collected information from those boards is sent over LoRa radio.

**Sensing/** Arduino code for SparkFun Redboard to interface with environmental sensor and accelerometer via QWIIC (i2c) interface.
