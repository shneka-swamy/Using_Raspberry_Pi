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


class Xbee():

    def __init__(self, portName, baudrate, address, apiMode=False, S1=False, timeout=2):
        self.serialPort = serial.Serial(portName, baudrate, timeout=timeout, rtscts=True)
        
        self.serialPort.reset_output_buffer()
        self.serialPort.reset_input_buffer()
        
    
        self.startDelimiter =  bytes([0x7E])
        self.destAddr


        xbeeBaudRate = self.getBaudRate()
        #Error occured configuring buad rate
        while(xbeeBaudRate == 0 or xbeeBaudRate == 1):
            if self.serialPort.baudrate == 250000:
                self.serialPort.baudrate = 115200
            elif self.serialPort.baudrate == 115200:
                self.serialPort.baudrate = 9600
            else:
                self.serialPort.baudrate = 250000
            
            time.sleep(2)
            xbeeBaudRate = self.getBaudRate()
            if xbeeBaudRate == 0 or xbeeBaudRate == 1: continue

            print(self.serialPort.baudrate)
            time.sleep(2)
            if self.desiredRate == 250000:
                self.setBaud250K()
            elif self.desiredRate == 115200:
                self.setBaud115k()
        print(self.serialPort.baudrate)
        self.enterCommandMode()
        self.setMinGaurdTime()
        self.writeChange()
        self.applyChanges()
        if address:
            self.setMy16BitAddress(address)
        self.setDH16Addr()
        if apiMode:
            self.enableAPIMode()
        else:
            self.enableTransparentMode()
        self.setTxPowerLevel(b'0')
        self.setMM()
        self.packetizationTimeout()
        self.flowControl(True)
        if(not S1):
            self.enableS1Compatability()
        self.setDH('00000000')
        self.writeChange()
        self.applyChanges()
        self.exitCommandMode()



    def __exit__(self, type, value, traceback):
        self.serialPort.close()
        return True

    #Command mode helper functions
    def enterCommandMode(self):
        """ Writes +++ to device
        Warning:: resets the input buffer
        """
        self.serialPort.reset_input_buffer()
        self.write(b'+++')
    
    def exitCommandMode(self):
        """ Writes ATCN """
        self.write(b'ATCN\r')

    def applyChanges(self, baudChange = None):
        """Applies changes with ATWR followed by ATAC
        :Params buardRate(optional) Will change serial port baud rate
        """
        self.write(b'ATWR\r')
        self.write(b'ATAC\r')
        if baudChange:
            self.serialPort.baudrate = baudChange

    def writeChange(self):
        self.write(b'ATWR\r')

    #Writes message to serial port. Catches error while in command mode
    def write(self, message):
        """ Writes and flushes message to xbee deives. Waits for response from device

        :param: message (bytes)
        :return: none
        :raises: CommunicationError
        """
        self.serialPort.write(message)
        self.serialPort.flush()
        if not self.validateCommandResponse():
            raise CommunicationError(message)


    def validateCommandResponse(self):
        """Check response from Xbee device
        :return: (boolean) 1. True->'OK\r' 2. False-> 'ERROR\r'
        """
        line = self.serialPort.read_until(b'\r')
        return b'OK' in line
    
    def getBaudRate(self):
        """Determines the serial baud rate stored in BD register
        :Warning Enters command mode automatically 
        :returns 0 -> error entering command mode, 1 -> Other error occured,
         None -> No error occured
         """
        try:
            self.enterCommandMode()
            self.serialPort.write(b'ATBD\r')
            baud_rate = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return baud_rate
        except CommunicationError as err:
            print("Error in getBaudRate caused by: %s, with baudRate: %s" %(err, self.serialPort.baudrate))
            if b'+++' in err.message:
                return 0
            else:
                return 1
        

    def setBaud250K(self):
        """Sets buard rate to 250000 
        :Warning enters command mode automatically
        :returns 0 -> error entering command mode, 1 -> Other error occured,
         None -> No error occured
         """
        try:
            self.enterCommandMode()
            #write 250000
            self.write(b'ATBD3D090\r')
            self.applyChanges(250000)
            self.exitCommandMode()
            return 
        except CommunicationError as err:
            print("Error in setBaud250k caused by: %s" %err)
            if b'+++' in err.message:
                return 0
            else:
                return 1

    def setBaud115k(self):
        """Sets buard rate to 250000 
        :Warning:: enters command mode automatically
        :returns: 1. 0 -> error entering command mode, 2. 1 -> Other error occured,
         3. None -> No error occured
         """
        try:
            self.enterCommandMode()
            #write 115200
            self.write(b'ATBD7\r')
            self.applyChanges(115200)
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setBaud115K caused by: %s" %err)
            if b'+++' in err.message:
                return 0
            else:
                return 1
 
    
    def enableAPIMode(self):
        """ Enters API Mode: See page 81 in user manual
        """
        try:
            self.write(b'ATAP1\r')
        except CommunicationError as err:
            print("Error in enableAPI caused by: %s" %err)
            return

    def enableTransparentMode(self):
        """Enters transparent mode: See page 81 in user manual
        """
        try:
            self.write(b'ATAP0\r')
        except CommunicationError as err:
            print("Error in enableTransparentMode caused by: %s" %err)
            return 

    
    def setMinGaurdTime(self):
        """Sets the guard time to the smallest possible value. page (241)
        """
        try:
            self.write(b'ATGT2\r')
        except CommunicationError as err:
            print("Error in setMinGaurdTime caused by: %s" %err)
            return        
    

    def setChannel(self, channelNumber):
        """Sets operation channel. See page 227
        :params byte in range 0x0B - 0x1A
        """
        try:
            if(channelNumber < 0x0B or channelNumber > 0x1A):
                return False
            message=(b'ATCH'+bytes(channelNumber,'ascii'))
            message+=b'\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in setChannel caused by: %s" %err)
            return 

    
    def setMM(self):
        try:
            message=b'ATMM2\r'
            self.write(message)
            self.applyChanges()
        except CommunicationError as err:
            print("Error in MM caused by: %s" %err)
            return 

    def enableS1Compatability(self):
        """Enables compatablity with S1 device"""
        try:
            message=b'ATC80\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in setChannel caused by: %s" %err)
            return 

    def packetizationTimeout(self):
        try:
            message=b'ATRO3\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in packetizationTimeout caused by: %s" %err)
            return

    def setDH16Addr(self):
        try:        
            self.write(b'ATDH00000000\r')
        except CommunicationError as err:
            print("Error in Set DH caused by: %s" %err)
            return 


    def setDH(self, address):

        try:
            message = b'ATDH'+bytes(address,'ascii')
            message+= b'\r'    
            self.write(message)
        except CommunicationError as err:
            print("Error in Set DH caused by: %s" %err)
            return 


    def setDL(self, address):
        if address == self.destAddr:
            return
        else:
            self.destAddr = address
        try:
            message = b'ATDL'+bytes(address,'ascii')
            message+= b'\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in setDL caused by: %s" %err)
            return 

    def setMy16BitAddress(self,address):
        try:
            message = (b'ATMY' + bytes(address, 'ascii'))
            message += b'\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in setting 16 bit addres caused by: %s" %err)
            return 

    def getMy16BitAddress(self):
        try:
            self.enterCommandMode()
            self.serialPort.write(b'ATMY\r')
            self.serialPort.flush()
            address = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return address
        except CommunicationError as err:
            print("Error in getting 16 bit addres caused by: %s"% err)
            return 


    def getDestAddr(self):
        """Returns desination address in the form of bytes"""
        try:
            self.serialPort.write(b'ATDL\r')
            address = self.serialPort.read_until(b'\r')
            return address
        except CommunicationError as err:
            print("Error in getting 16 bit addres caused by: %s"% err)
            return    
    
    def flowControl(self, enableFlag):
        """Enables or disables RTS/CTS flow control. See page 43
        :params: enableFlag (boolen) 1.True-> enable flow control
        2. False -> disable flow control
        """
        try:
            if(enableFlag):
                self.write(b'ATD71\r')
                self.write(b'ATD61\r')
            else:
                self.write(b'ATD70\r')
                self.write(b'ATD60\r')

        except CommunicationError as err:
            print("Error in flowControl caused by: %s"% err)
            return 


    def setTxPowerLevel(self, powerLevel):
        """Sets Tx Power level
        :Params bytes in range 0-4
        """
        try:
            if(powerLevel < b'0' or powerLevel > b'4'):
                return False
            message=(b'ATPL'+powerLevel)
            message+=b'\r'
            self.write(message)
        except CommunicationError as err:
            print("Error in setTxPowerLevel caused by: %s" %err)
            return 

    def create16BitAddrFrame(self, data, address=0x0000,  mode=0, stringData=True):
        """Creates frame to API Specification. Working but not verifed recently
        """
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
        """Reads API frame"""
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
        

    def transmitSerialData(self, data, address, stringData = True):
        """Creates API frame before transmitting
        """
        frame = self.create16BitAddrFrame(data, address=address, mode=0, stringData=stringData)
        self.serialPort.write(frame)

    def transmit(self, data, address):
        """Transmits data to address specified. Changes address if it does not match
        """
        
        if address == self.destAddr:
            pass
        else:
            self.enterCommandMode()
            self.setDL(address)
            self.write(b'ATAC\r')
            self.exitCommandMode()

        self.serialPort.write(data)
        self.serialPort.flush()

    def read(self, packetSize=32):
        """Reads bytes from input buffer
        :Params packetSize=32; configurable to read number of bytes from input buffer
        :Returns bytes from input buffer
        """
        return self.serialPort.read(packetSize)


