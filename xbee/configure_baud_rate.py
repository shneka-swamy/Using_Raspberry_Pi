import serial
import time

from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *



class Xbee_Initialization:
    def __init__(self, port_name='/dev/ttyUSB0', baud_rate=115200, timeout=2.5):
        self.port_name = port_name
        self.timeout=timeout
        with serial.Serial(port_name, baud_rate, timeout=self.timeout) as self.ser:
            if self._set_xbee_max_baud():
                print('115200')
                baud_rate = 250000
                self.ser.baudrate = baud_rate
            else:
                print('NOT 115200')
                if self._test_max_baud_rate():
                    baud_rate = 250000
                    self.ser.baudrate = baud_rate
                else:
                    print("Wrong baud rate! Exitint with Error")i
                    return

            if self._enable_api_mode():
                print("Entered API Mode")

    def getXbeeDevice(self):
        return self.xbee

    def get_baud_rate(self, baud_rate):
        with serial.Serial(self.port_name, baud_rate, timeout=self.timeout) as self.ser:
            self.ser.write(b'+++')
            if not self._verify_response():
                return False

            self.ser.write(b'ATBD\r')
            print(self.ser.readline())
            self.ser.write(b'ATCN\r')



    def _verify_response(self):
        line = self.ser.readline()
        return b'OK' in line

    def _set_xbee_max_baud(self):
        self.ser.write(b'+++')
        if not self._verify_response():
            return False

        self.ser.write(b'ATBD3D090\r')
        if not self._verify_response():
            return False


        self.ser.write(b'ATAC\r')
        if not self._verify_response():
            return False     

        self.ser.write(b'ATWR\r')
        if not self._verify_response():
            return False

        self.ser.write(b'ATCN\r')
        time.sleep(5)
        return True
    
    def _enable_api_mode(self):
        self.ser.write(b'+++')
        if not self._verify_response():
            return False 

        self.ser.write(b'ATAP1\r')
        if not self._verify_response():
            return False 
        
        self.ser.write(b'ATWR\r')
        if not self._verify_response():
            return False

        self.ser.write(b'ATAC\r')
        if not self._verify_response():
            return False 
        self.ser.write(b'ATCN\r')

        return True        

    def _test_max_baud_rate(self):
        start_baudrate = self.ser.baudrate 
        self.ser.baudrate = 250000

        self.ser.write(b'+++')        
        message_success = self._verify_response()
        if message_success:
             self.ser.write(b'ATCN\r')
             time.sleep(2)
        else:
            self.ser.baudrate = start_baudrate
        return message_success



