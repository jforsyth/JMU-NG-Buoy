import serial
from serial.tools.list_ports import comports


ports_list = comports()

print("Available COM ports are: ")
for port in ports_list:
    print(port.device)


port_name = "/dev/cu.usbmodem1451401"

# print("Opening port " + port_name)
port = serial.Serial(port_name, baudrate=57600, timeout=5)

while True:
    line = port.readline()

    line = line.decode('utf-8')
    line = line.replace('\r', '').replace('\n', '')

    data = line.split(",")
    length = len(data)

    if len(data)==1:
        #this is a dummy message
        continue
    else:
        #parse message and print pretty thing
        latitude = float(data[0])
        longitude = float(data[1])
        humidity = int(data[2])
        pressure = int(data[3])
        altitude = float(data[4])
        temperature = float(data[5])
        xAccel = float(data[6])
        yAccel = float(data[7])
        zAccel = float(data[8])

        print("Location: " + str(latitude) + "," + str(longitude))
        print("Environmental Conditions: " + "Humdity: " + str(humidity) + " Pressure: " + str(
            pressure) + " Altitude: " + str(altitude)
              + " Temp: " + str(temperature) + " xAccel: " + str(xAccel) + " yAccel: " + str(yAccel) + " zAccel: " + str(
            zAccel))


port.close()