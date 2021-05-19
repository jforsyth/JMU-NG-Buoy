## Original program based upon Adafruit Ultimate GPS Demo
## https://github.com/adafruit/Adafruit_CircuitPython_GPS/blob/master/examples/gps_simpletest.py
##
## Modificcations made by Collete Higgins and Jason Forsyth (forsy2jb@jmu.ed)
##
##
## SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
## SPDX-License-Identifier: MIT

#needed to count time
import time

#can only be installed via pip install adafruit-circuitpython-gps (at the moment)
import adafruit_gps

#import serial via PySerial
import serial

# encode separation comma
az = ','
cz = b','
dz = az.encode('ASCII')
if (dz == cz):
    print("ENCODING SUCCESSFUL")
else:
    print("encoding unsuccessful")

#add in code to search for USB...
serial_port_name="/dev/cu.usbserial-0221246F"

#create serial instance to talk with USB GPS
uart = serial.Serial(serial_port_name, baudrate=9600, timeout=10)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once every 1000ms (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")


# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()

    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:

            # Try again if we don't have a fix yet.
            print("Waiting for fix...")

            #continue to loop (while)
            continue

        # print the lat and long to the PI screen up to 6 decimal places
        print("Lat: {0:.6f}".format(gps.latitude))
        print("Long: {0:.6f}".format(gps.longitude))

        ##prepare data for transmission through Radio connected via USB

        # limit decimal places of latitude and longitude
        limited_lat = "{:.6f}".format(gps.latitude)
        limited_long = "{:.6f}".format(gps.longitude)

        # convert from float to string
        lat_in_string = str(limited_lat)
        long_in_string = str(limited_long)

        # concatenate string
        gps_string = lat_in_string + "," + long_in_string

        # convert from string to bytes
        gps_data = str.encode(gps_string)

        # send data down USB port to radio.
        #data_out_port.write(gps_data)

print("Show's over. Close the ports!")

uart.close()