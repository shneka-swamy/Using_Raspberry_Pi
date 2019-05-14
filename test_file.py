# This program checks if the serial port communication is set properly between the raspberry pi and the xbee hardware.
# This program is taken from https://www.raspberrypi.org/forums/viewtopic.php?t=172194

import serial
import time

ser = serial.Serial("/dev/ttyS0", buadrate= 9600)

while True:
  data = ser.readline()
  print(data)
