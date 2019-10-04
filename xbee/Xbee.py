import digi
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.models.status import NetworkDiscoveryStatus

class Xbee:
    
    def __init__(self, portName, baudrate):
        self.xbee = XBeeDevice(portName, baudrate)
        self.xbee.open()
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.xbee.close()

    
    def setNodeId(self):

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
        pass
