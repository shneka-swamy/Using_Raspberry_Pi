import serial
import io
import time
import sys

class Error(Exception):
    pass

class CommunicationError(Error):
    """Exception raised for errors in the response from xbee.

    Attributes:
        expression -- input that in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class XbeeInitialization():

    def __init__(self, portName, baudrate):
        self.serialPort = serial.Serial(portName, baudrate, timeout=2)
        self.sio = io.BufferedRWPair(self.serialPort,self.serialPort, 1)
        self.serialPort.reset_output_buffer()
        self.serialPort.reset_input_buffer()

    def __exit__(self, type, value, traceback):
        print(traceback, value)
        self.serialPort.close()
        return True

    #Command mode helper functions
    def enterCommandMode(self):
        self.write(b'+++')
    
    def exitCommandMode(self):
        self.write(b'ATCN\r')

    def applyChanges(self):
        self.write(b'ATAC\r')
        self.write(b'ATWR\r')

    #Writes message to serial port. Catches error while in command mode
    def write(self, message):
        self.serialPort.write(message)
        self.serialPort.flush()
        if not self.validateCommandResponse():
            raise CommunicationError(message)

    def validateCommandResponse(self):
        line = self.serialPort.read_until(b'\r')
        return b'OK' in line
    
    def getBaudRate(self):
        try:
            self.enterCommandMode()
            self.serialPort.read_until(b'\r')
            self.write(b'ATBD\r')
            baud_rate = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return baud_rate
        except CommunicationError as err:
            print("Error in getBaudRate caused by: %s"% err)
            return 
        

    def setMaxBaud(self):
        try:
            self.enterCommandMode()
            #write 250000
            self.write(b'ATBD3D090\r')
            self.applyChanges()
            self.exitCommandMode()
            self.serialPort.baudrate = 250000

        except CommunicationError as err:
            print("Error in setMaxBaud caused by: %s" %err)
            return 
            
    def enableAPIMode(self):
        try:
            self.enterCommandMode()
            self.write(b'ATAP2\r')
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            #print(f"Error in setMaxBaud caused by: {err}")
            return 

    def readSerialData(self):
        data = self.serialPort.read(32)

    def transmitSerialData(self, data):
        self.serialPort.write(data)
        self.serialPort.flush()




def main():
    PORT_NAME = '/dev/ttyS0'
    baudrate = int(sys.argv[1])
    xbee = XbeeInitialization(PORT_NAME, baudrate)
    print(f"Xbee online @{xbee.getBaudRate()} baud")
    mode = input("(T)x or (R)x")

    if mode == "T":
        print("Entered tranmitter mode")
        while(True):
            xbee.transmitSerialData(b"Hello Xbee")
            time.sleep(2)
    else:
        print("Entered Rx mode")
        while(True):
            print(xbee.readSerialData())

if __name__ == '__main__':
    main()