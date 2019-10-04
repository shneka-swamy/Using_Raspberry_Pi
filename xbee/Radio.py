import traceback
from InitRadio import XbeeInitalization
from xbee_interface import Xbee
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *
import sys

def data_receive_callback(xbee_message):
    not_used =  xbee_message.data.decode()

def main():
    print(sys.path)
    PORT_NAME = '/dev/ttyUSB0'
    BAUDRATE = 250000
    try:
        with XBeeDevice(PORT_NAME,BAUDRATE) as xbee:
            print(xbee.get_node_id())
    except:
        traceback.print_last()
        print("Error opeing device; Configuring baudrate")
        try:
            with XbeeInitalization(PORT_NAME, BAUDRATE) as commPort:
                commPort.setMaxBaud()
                commPort.enableAPIMode()
        except:
            traceback.print_last()


if __name__ == '__main__':
    main()






