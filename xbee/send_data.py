from digi.xbee.devices import *
from XbeeModule import *
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():

	parser = argparse.ArgumentParser(description='audio player')
	parser.add_argument('--addr', action='store', dest='address', type=str, help='16 bit address')
	parser.add_argument('--port', action='store', dest='portName', default='/dev/ttyUSB0')
	parser.add_argument('--rate', action='store', dest='baudRate', type=int, default=250000)
	parser.add_argument('--api', action='store', dest='apiMode', type=str2bool, default=False)
	parser.add_argument('--s1', action='store', dest='S1Mode', type=str2bool, default=False)
	args = parser.parse_args()


	xbee_1 = Xbee(args.portName, args.baudRate, args.address, args.apiMode, args.S1Mode)

	xbee_1.setDH('00000000')
	
	xbee_1.transparentTransmit(b'Hello','CCCC')


	#print(xbee_2.transparentRead()) 

if __name__ == '__main__':
	main()