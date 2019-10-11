import traceback

from XbeeInitialization import * 
from Xbee import *

import sys

class Radio():

    def __init__(self):
        self.PORT_NAME = '/dev/ttyUSB0'
        self.BAUDRATE = 250000
        self.try_opening()


    def try_opening(self):
        
        with XbeeInitialization(self.PORT_NAME, 115200) as ser:
            print(ser.getBaudRate())

def main():
    PORT_NAME = '/dev/ttyUSB0'
    BAUDRATE = 115200
    with XbeeInitialization(PORT_NAME, BAUDRATE) as xbee:
        xbee.setMaxBaud()
    

"""
        try:
            with Xbee(self.PORT_NAME,self.BAUDRATE) as self.xbee:
                print(self.xbee.read_deivce_info())
        except InvalidOperatingModeException:
            self.xbee.reset()
            try_opening()
        """
"""
            print("Error opeing device; Configuring baudrate")
            try:
                possible_buad_rates = [9600, 56000, 115200, 250000]
                for rate in possible_buad_rates:
                    
            except:
                #traceback.print_last()
                print("also error here")
                pass"""








