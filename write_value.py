#This program uses the digi xbee library.

from digi.xbee.devices import XBeeDevice

device = XBeeDevice("/dev/ttyS0",9600)
device.open()

#To broadcast the message use

device.send_data_broadcast("Hello Xbee :)")

