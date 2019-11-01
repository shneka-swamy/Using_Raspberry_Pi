import serial
import io
import time
import random
import sys


class message():
    def __init__(self, sender, data):
        self.sender = sender
        self.data = data

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
        self.startDelimiter =  bytes([0x7E])

    def __exit__(self, type, value, traceback):
        print(traceback, value)
        self.serialPort.close()
        return True

    #Command mode helper functions
    def enterCommandMode(self):
        self.serialPort.reset_input_buffer()
        self.write(b'+++')
    
    def exitCommandMode(self):
        self.write(b'ATCN\r')

    def applyChanges(self, baudChange = None):
        self.write(b'ATWR\r')
        self.write(b'ATAC\r')
        if baudChange:
            self.serialPort.baudrate = baudChange

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
            self.serialPort.write(b'ATBD\r')
            baud_rate = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return baud_rate
        except CommunicationError as err:
            print("Error in setMaxBaud caused by: %s" %err)
            if b'+++' in err.message:
                return 0
            else:
                return 1
        

    def setMaxBaud(self):
        try:
            self.enterCommandMode()
            #write 250000
            self.write(b'ATBD3D090\r')
            self.applyChanges(250000)
            self.exitCommandMode()
            return 
        except CommunicationError as err:
            print("Error in setMaxBaud caused by: %s" %err)
            if b'+++' in err.message:
                return 0
            else:
                return 1

    def setBaudto115k(self):
        try:
            self.enterCommandMode()
            #write 115200
            self.write(b'ATBD1C200\r')
            self.applyChanges(115200)
            self.exitCommandMode()

        except CommunicationError as err:
            print("Error in setBaudTo115K caused by: %s" %err)
            return    
    def enableAPIMode(self):
        try:
            self.enterCommandMode()
            self.write(b'ATAP1\r')
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in enableAPI caused by: %s" %err)
            return 

    def set16BitAddress(self,address):
        try:
            self.enterCommandMode()
            message = (b'ATMY' + bytes(address, 'ascii'))
            message += b'\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setting 16 bit addres caused by: %s" %err)
            return 

    def get16BitAddress(self):
        try:
            self.enterCommandMode()
            self.serialPort.write(b'ATMY\r')
            address = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return address
        except CommunicationError as err:
            print("Error in getting 16 bit addres caused by: %s"% err)
            return 

    def setChannel(self):
        pass
    def scanChannels(self):
        pass

    def setTxPowerLevel(self, powerLevel):
        pass

    def create16BitAddrFrame(self, data, address=0x0000,  mode=0, stringData=True):
        
        frameType = 0x01
        frameID = 0x01
        #convert string data to byte array
        if stringData:
            data = bytes(data, 'ascii')
        
        address = bytes([((address >> 8) & 0xff), address & 0xff])

        #Choose tranmission type
        if mode == 0:
            #Sync message: expect acknowledgement
            options = 1 
        elif mode == 1:
            #async message
            options = 0
        elif mode == 2:
            options = 4
        
        options = 0
        frame = bytes([frameType, frameID])
        frame += address
        frame += bytes([options])
        frame += data

        length = len(frame)
        if length < 255:
            lengthBytes = bytes([0, len(frame)])
        else:
            lengthBytes = bytes([len(frame)])
        
        checkSum = 0
        for i in frame:
            checkSum += i
        checkSum = 255- (checkSum & 0xFF)
        checkSumBytes=bytes([checkSum])
        frame = self.startDelimiter + lengthBytes + frame + checkSumBytes
        return frame


    def readSerialData(self):
        #Starting delimiter
        startingDelimiter = self.serialPort.read(1)
        if startingDelimiter != self.startDelimiter:
            return
        numBytes = int.from_bytes(self.serialPort.read(2),byteorder='big', signed=False)
        #number that im not sure about yet
        self.serialPort.read(1)


        sender = int.from_bytes(self.serialPort.read(2),byteorder='big', signed=False)
        #Another two im not sure about
        self.serialPort.read(2)
        data = self.serialPort.read(numBytes)
        #Check sum
        self.serialPort.read(1)
        return(message(sender,data))
        

    def transmitSerialData(self, data, address):
        frame = self.create16BitAddrFrame(data, address=address, mode=0, stringData=True)
        self.serialPort.write(frame)


def resetBaud():
    if sys.argv[2] == '-i':
        incrementArgs = 1
    else:
        incrementArgs = 0
    PORT_NAME = sys.argv[2+incrementArgs]
    baudrate = int(sys.argv[1+incrementArgs])
    xbee = XbeeInitialization(PORT_NAME, baudrate)
    xbee.setBaudto115k()
    time.sleep(1.5)
    print(xbee.getBaudRate())

def test():
    if sys.argv[2] == '-i':
        incrementArgs = 1
    else:
        incrementArgs = 0
    PORT_NAME = sys.argv[2+incrementArgs]
    baudrate = int(sys.argv[1+incrementArgs])
    xbee = XbeeInitialization(PORT_NAME, baudrate)
    xbeeBaudRate = xbee.getBaudRate()
    if xbeeBaudRate == 0:
        xbee.serialPort.baudrate = 115200
        xbee.setMaxBaud()
        xbeeBaudRate = xbee.getBaudRate()
    elif xbeeBaudRate == 1:
        print("Baud rate was not %s, trying 115200" %baudrate)
        xbee.serialPort.baudrate = 115200
        if xbee.getBaudRate():
            time.sleep(1.6)
            xbee.setMaxBaud()
            xbeeBaudRate = xbee.getBaudRate()
            print("Error resolved: Baud rate now set to 250000")
        else:
            print("error with xbee initial baud rate, exiting program")
    #Needs to 2 seoncds for radio to settle
    time.sleep(1.5)
    xbee.set16BitAddress(sys.argv[3+incrementArgs])
    time.sleep(1.5)
    xbee.enableAPIMode()
    time.sleep(1.5)
    address = xbee.get16BitAddress()
    print("Xbee online @%s baud and addressed as %s" %(str(xbeeBaudRate).strip(), str(address).strip()))
    mode = input("(T)x or (R)x")

    if mode == "T":
        print("Entered tranmitter mode")
        while(True):
            xbee.transmitSerialData("hello xbee", 0xBBBB)
    else:
        print("Entered Rx mode")
        data = []
        while(True):
            message = xbee.readSerialData()
            if message:
                data.append(message)
                print(len(data))

if __name__ == '__main__':
    test()