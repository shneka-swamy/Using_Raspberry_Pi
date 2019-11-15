from digi.xbee.devices import *
from XbeeModule import *

def main():
	xbee_1 = Xbee("/dev/ttyUSB0", 250000, 'AAAA', False, True)
	#xbee_2 = Xbee("/dev/ttyUSB1", 250000, 'BBBB', False)

	xbee_1.setDH('00000000')
	xbee_1.setDL('0000BBBB')
	xbee_1.transparentTransmit(b'Hello','BBBB')


	#print(xbee_2.transparentRead()) 

if __name__ == '__main__':
	main()