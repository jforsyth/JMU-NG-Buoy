import serial
from serial.tools.list_ports import comports

import time

# can only be installed via pip install adafruit-circuitpython-gps (at the moment)
import adafruit_gps


# attempt to open each one. If the first thing received is an '@' it's the environmental
# board. If that is what is not received, it's not the com port. If it times out, nothing is home.
def identify_ports():
    ports_list = comports()

    gps_device = -1
    sensing_device = -1

    for port_candidate in ports_list:
        port_name = port_candidate.device
        try:
            # print("Opening port " + port_name)
            port = serial.Serial(port_name, baudrate=9600, timeout=5)

            # print("Attempting read...")
            line = port.readline()

            # print("Read: "+line)
            # line = bytes.decode('utf-8')
            # line = line.replace('\r', '').replace('\n', '')

            if len(line) == 0:
                # print("Nothing read...")
                continue

            line = line.decode('utf-8')
            line = line.replace('\r', '').replace('\n', '')
            # print(line)

            splits = line.split(",")

            if splits[0] == '@':
                # print("Found the Sensing board...")
                sensing_device = port_name
            elif '$' in splits[0]:
                # print("Found the GPS board...")
                gps_device = port_name
            else:
                # print("Unknown board..")
                do_nothing = 0

            port.close()
        except:
            # print("Exception occurred.")
            do_nothing = 0

    return gps_device, sensing_device

def get_GPS_update(gps):
    if not gps.has_fix:
        # Try again if we don't have a fix yet.
        #print("Waiting for fix...")

        # continue to loop (while)
        return -1,-1

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

    return lat_in_string, long_in_string

def get_environment_update(port):
    ##read until line new line
    bytes = port.readline()

    # decode bytes into string
    line = bytes.decode('utf-8')
    line = line.replace('\r', '').replace('\n', '')

    # print out the line to the terminal that was received
    # print(line)

    # split data into various elements, first element should be '@'
    data = line.split(",")

    if len(data) != 8:
        print("Invalid string received!")
        return -1

    else:
        # copy the string information into variables
        humidity = int(data[1])
        pressure = int(data[2])
        altitude = float(data[3])
        temp = float(data[4])
        xAccel = float(data[5])
        yAccel = float(data[6])
        zAccel = float(data[7])

    return (humidity,pressure,altitude,temp,xAccel,yAccel,zAccel)

if __name__ == "__main__":

    print("Hello world! Welcome to the Raspberry Pi Buoy Program...")

    ##
    # Scan attached ports to identify the "correct" ones for each device.
    ##
    print("Scanning serial ports to identify connected devices...")

    gps_port_name = -1
    sensing_port_name = -1

    (gps_port_name, sensing_port_name) = identify_ports()

    if gps_port_name == -1:
        print("Could not locate GPS port!")
    else:
        print("Found gps on port: " + gps_port_name)

    if sensing_port_name == -1:
        print("Could not locate Arduino Sensing port!")
    else:
        print("Found Arduino sensing board on port: " + sensing_port_name)

    ##
    # Open serial ports for all devices
    ##

    ##attempt to load GPS unit
    try:
        gps_serial_port = serial.Serial(gps_port_name, baudrate=9600, timeout=10)
    except:
        print("Failure opening GPS port!")
        exit(-1)

    ##attempt to load Arduino sensing unit
    try:
        sensing_serial_port = serial.Serial(sensing_port_name, baudrate=9600, timeout=10)
    except:
        print("Failure opening Arduino Sensing port!")

    ##
    # Configure GPS Unit via Adafruit GPS Library
    ##

    # Create a GPS module instance.
    gps_object = adafruit_gps.GPS(gps_serial_port, debug=False)  # Use UART/pyserial

    # Turn on the basic GGA and RMC info (what you typically want)
    gps_object.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once every 1000ms (1hz) which is what you typically want.
    gps_object.send_command(b"PMTK220,1000")

    ##
    # Big loop to run program forever.
    ##

    last_print = currentTime = int(time.time())
    while True:
        # Make sure to call gps.update() every loop iteration and at least twice
        # as fast as data comes from the GPS unit (usually every second).
        # This returns a bool that's true if it parsed new data (you can ignore it
        # though if you don't care and instead look at the has_fix property).
        gps_object.update()

        # Keep track of loop timing
        currentTime = int(time.time())

        #get the latest latitude and longitude
        (latitude, longitude) = get_GPS_update(gps_object)

        #get the latest environmental information
        (humidity,pressure,altitude,temp,xAccel,yAccel,zAccel) = get_environment_update(sensing_serial_port)


        #print out a message every so often
        if currentTime - last_print >= 1.0:
            last_print=currentTime

            print("Location: " + str(latitude) + "," + str(longitude))
            print("Environmental Conditions: "+"Humdity: "+str(humidity)+" Pressure: "+str(pressure)+" Altitude: "+str(altitude)
          +" Temp: "+str(temp)+" xAccel: "+str(xAccel)+" yAccel: "+str(yAccel)+" zAccel: "+str(zAccel))



