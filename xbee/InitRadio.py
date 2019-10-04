import serial
import time


class Error(Exception):
    pass

class CommunicationError(Error):
    """Exception raised for errors in the response from xbee.

    Attributes:
        expression -- input that in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __repr__(self):
        return self.message


class XbeeInitalization:

    def __init__(self, portName, baudrate):
        self.serialPort = serial.Serial(portName, baudrate, timeout=self.timeout)
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        print(traceback, value)
        self.serialPort.close()
        return True

    def write(self, message):
        self.serialPort.write(message)
        if not self.verifyResponse():
            raise CommunicationError(message)

    def verifyResponse(self):
        line = self.ser.readline()
        return b'OK' in line
    
    def getBaudRate(self, baud_rate):
        try:
            self.write(b'+++')
            self.serialPort.write(b'ATBD\r')
            baud_rate = self.serialPort.readline()
            self.serialPort.write(b'ATCN\r')
            return baud_rate
        except CommunicationError as err:
            print("Error in getBaudRate caused by: {err}")
            return 
        

    def setMaxBaud(self):
        try:
            self.write(b'+++')
            #write 250000
            self.write(b'ATBD3D090\r')
            self.write(b'ATAC\r')  
            self.write(b'ATWR\r')
            self.write(b'ATCN\r')

        except CommunicationError as err:
            print("Error in setMaxBaud caused by: {err}")
            return 
            
    def enableAPIMode(self):
        try:
            self.write(b'+++')
            self.write(b'ATAP1\r')
            self.write(b'ATWR\r')
            self.write(b'ATAC\r')
            self.write(b'ATCN\r')
        except CommunicationError as err:
            print("Error in setMaxBaud caused by: {err}")
            return 