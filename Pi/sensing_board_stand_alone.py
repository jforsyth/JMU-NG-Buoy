import serial

import time

#add in code to search for USB...
serial_port_name="/dev/cu.usbserial-143130"

#create serial instance to talk with USB GPS
uart = serial.Serial(serial_port_name, baudrate=9600, timeout=10)

print("Running a demo for 10s...")
startTime = currentTime = int(time.time())

#data from environmental board on Arduino https://www.sparkfun.com/products/14348
humidity=-1  #relative humidity measured
pressure=-1 #measured in Pascals
altitude=-1 #measured in meters
temperature = -1 #measured in Fahrenheit

#data from accelerometer on Arduino https://www.sparkfun.com/products/14587
xAccel = -1 #x-acceleration measured in g's
yAccel = -1 #y-acceleration measured in g's
zAccel = -1 #z-acceleration measured in g's

while True:

    ##read until line new line
    bytes = uart.readline()

    # decode bytes into string
    line = bytes.decode('utf-8')
    line = line.replace('\r', '').replace('\n', '')

    # print out the line to the terminal that was received
    #print(line)

    #split data into various elements, first element should be '@'
    data = line.split(",")

    if len(data) != 8:
        print("Invalid string received!")
        continue
    else:
        #copy the string information into variables
        humidity=int(data[1])
        pressure=int(data[2])
        altitude=float(data[3])
        temp=float(data[4])
        xAccel=float(data[5])
        yAccel=float(data[6])
        zAccel=float(data[7])

    print("Humdity: "+str(humidity)+" Pressure: "+str(pressure)+" Altitude: "+str(altitude)
          +" Temp: "+str(temp)+" xAccel: "+str(xAccel)+" yAccel: "+str(yAccel)+" zAccel: "+str(zAccel))

    # keep track of current time
    currentTime = int(time.time())

print("Show's over. Close the ports!")

uart.close()

print("Done!")