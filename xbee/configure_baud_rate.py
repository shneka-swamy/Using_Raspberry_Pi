import serial
import time

from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *



class Xbee_Initialization:
    def __init__(self, port_name='/dev/ttyUSB0', baud_rate=115200, timeout=1):
        with serial.Serial(port_name, baud_rate, timeout=timeout) as self.ser:
            if self._set_xbee_max_baud_():
                baud_rate = 250000
                self.ser.baudrate = baud_rate
            else:
                if self._test_max_baud_rate_():
                    baud_rate = 250000
                    self.ser.baudrate = baud_rate
                else:
                    print("Wrong baud rate!")
                    return
            
            if self._enable_api_mode_():
                self.xbee = XBeeDevice(port_name, baud_rate)
                try:
                    self.xbee.open()
                except InvalidOperatingModeException:
                    print("Reset Device!")
            else:
                print("Error Entering API mode")
                return None

            
    def getXbeeDevice(self):
        return self.xbee

    def _verify_response_(self, time_delay):
        time.sleep(time_delay)
        line = self.ser.readline()
        print(line)
        return b'OK' in line

    def _set_xbee_max_baud_(self):
        self.ser.write(b'+++')
        
        if not self._verify_response_(2):
            return False

        self.ser.write(b'ATWR\r')
        if not self._verify_response_(.5):
            return False

        self.ser.write(b'ATBD3D090\r')
        if not self._verify_response_(.5):
            return False

        self.ser.write(b'ATAC\r')
        if not self._verify_response_(.5):
            return False 

        self.ser.write(b'ATCN\r')
        time.sleep(5)
        return True
    
    def _enable_api_mode_(self):
        self.ser.write(b'+++')
        if not self._verify_response_(2):
            return False 

        self.ser.write(b'ATAP2\r')
        if not self._verify_response_(.5):
            return False 
        self.ser.write(b'ATAC\r')
        if not self._verify_response_(.5):
            return False 
        self.ser.write(b'ATCN\r')

        return True        

    def _test_max_baud_rate_(self):
        start_baudrate = self.ser.baudrate
        self.ser.baudrate = 250000

        self.ser.write(b'+++')        
        message_success = self._verify_response_(1.5)
        if message_success:
             self.ser.write(b'ATCN\r')
             time.sleep(2)
        else:
            self.ser.baudrate = start_baudrate
        return message_success



