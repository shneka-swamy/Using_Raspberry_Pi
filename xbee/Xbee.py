import digi
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.exception import *

class Xbee:
    
    def __init__(self, portName, baudrate):
        self.xbee = XBeeDevice(portName, baudrate)
        
    def __enter__(self):
        self.xbee.open()
        return self.xbee
    def __exit__(self, exc_type, value, traceback):
        print("totally caught that error")
        print(f"{exc_type}, {value}, {traceback}")
        self.xbee.close()

    
    """ def setNodeId(self):

        pass

    def measureRSSI(self):
        pass

    def unicast(self,address) -> bool:
        pass
    def broadcast(self) -> bool:
        pass
        
    def multicast(self,*addresses) -> bool:
        pass

    def recieve_callback(self) -> int:
        pass


    def discover_network(self) -> list:
        pass

    def set_power(self,power_level) -> bool:
        pass"""
