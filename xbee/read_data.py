from digi.xbee.devices import *
from XbeeModule import *

def main():
	#xbee_1 = Xbee("/dev/ttyUSB0", 250000, 'AAAA', False)
	xbee_2 = Xbee("/dev/ttyUSB1", 250000, 'BBBB', False, True)

	#xbee_1.transparentTransmit(b'Hello','BBBB')

	while True:
		data = xbee_2.transparentRead()

		if data != None:
			print(data)

if __name__ == '__main__':
	main()