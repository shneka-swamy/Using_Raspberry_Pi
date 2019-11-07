from XbeeModule import Xbee
import argparse



parser = argparse.ArgumentParser(description='audio player')

parser.add_argument('--addr', action='store', dest='address', type=str, help='16 bit address')
parser.add_argument('--port', action='store', dest='portName', default='/dev/ttyS0')
parser.add_argument('--rate', action='store', dest='baudRate', type=int, default=250000)
parser.add_argument('--api', action='store', dest='apiMode', type=bool, default=False)
args = parser.parse_args()


xbee = Xbee(args.portName, args.baudRate, args.address, args.apiMode)

print(xbee.getMy16BitAddress())
print(xbee.getBaudRate())