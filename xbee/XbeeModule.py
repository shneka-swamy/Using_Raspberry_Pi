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

    def __init__(self, portName, baudrate, address, apiMode):
        self.serialPort = serial.Serial(portName, baudrate, timeout=2)
        self.sio = io.BufferedRWPair(self.serialPort,self.serialPort, 1)
        self.serialPort.reset_output_buffer()
        self.serialPort.reset_input_buffer()
        
    
        self.startDelimiter =  bytes([0x7E])
        self.destAddr = b''
        
        xbeeBaudRate = self.getBaudRate()
        #Error occured configuring buad rate
        while(xbeeBaudRate ==0 or xbeeBaudRate == 1):
            if self.serialPort.baudrate == 250000:
                self.serialPort.baudrate = 115200
            elif self.serialPort.baudrate == 115200:
                self.serialPort.baudrate = 9600
            else:
                self.serialPort.baudrate = 250000
                print("Buad rate error")

            print(baudrate)
            print(self.serialPort.baudrate)
            if baudrate == 250000:
                self.setMaxBaud()
            elif baudrate == 115200:
                self.setBaudto115k()

            time.sleep(1.2)
            xbeeBaudRate = self.getBaudRate()
            

        time.sleep(1.1)
        self.setMinGaurdTime()
        time.sleep(1.1)
        if address:
            self.setMy16BitAddress(address)
        time.sleep(1.1)
        self.setDH16Addr()
        time.sleep(1.1)
        if apiMode:
            self.enableAPIMode()
        else:
            self.enableTransparentMode()
        #time.sleep(1.1)
        #self.address = self.getMy16BitAddress()
        time.sleep(1.1)
        self.setTxPowerLevel(b'0')
        time.sleep(1.1)
        self.setMM()
        time.sleep(1.1)
        self.enableS1Compatability()
        time.sleep(1.1)


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

    def writeChange(self):
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

    def enableTransparentMode(self):
        try:
            self.enterCommandMode()
            self.write(b'ATAP0\r')
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in enableTransparentMode caused by: %s" %err)
            return 

    
    def setMinGaurdTime(self):
        try:
            self.enterCommandMode()
            self.write(b'ATGT2\r')
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setMinGaurdTime caused by: %s" %err)
            return        
    

    def setChannel(self, channelNumber):
        try:
            if(channelNumber < 0xB or channelNumber > 0x1A):
                return False
            self.enterCommandMode()
            message=(b'ATCH'+bytes(channelNumber,'ascii'))
            message+=b'\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setChannel caused by: %s" %err)
            return 

    
    def setMM(self):
        try:
            self.enterCommandMode()
            message=b'ATMM2\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in MM caused by: %s" %err)
            return 

    def enableS1Compatability(self):
        try:
            self.enterCommandMode()
            message=b'ATC80\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setChannel caused by: %s" %err)
            return 


    def setDH16Addr(self):
        try:
            self.enterCommandMode()        
            self.write(b'ATDH00000000\r')
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in Set DH caused by: %s" %err)
            return 


    def setDH(self, address):

        try:
            self.enterCommandMode()
            message = b'ATDH'+bytes(address,'ascii')
            message+= b'\r'    
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in Set DH caused by: %s" %err)
            return 


    def setDL(self, address):
        if address == self.destAddr:
            return
        else:
            self.destAddr = address
        try:
            self.enterCommandMode()
            message = b'ATDL'+bytes(address,'ascii')
            message+= b'\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setDL caused by: %s" %err)
            return 

    def setMy16BitAddress(self,address):
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

    def getMy16BitAddress(self):
        try:
            self.enterCommandMode()
            self.serialPort.write(b'ATMY\r')
            address = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return address
        except CommunicationError as err:
            print("Error in getting 16 bit addres caused by: %s"% err)
            return 


    def getDestAddr(self):
        try:
            self.enterCommandMode()
            self.serialPort.write(b'ATDL\r')
            address = self.serialPort.read_until(b'\r')
            self.exitCommandMode()
            return address
        except CommunicationError as err:
            print("Error in getting 16 bit addres caused by: %s"% err)
            return        

    def scanChannels(self):
        pass

    def clearChannelAssesment(self):
        pass

    def setTxPowerLevel(self, powerLevel):
        try:
            if(powerLevel < b'0' or powerLevel > b'4'):
                return False
            self.enterCommandMode()
            message=(b'ATPL'+powerLevel)
            message+=b'\r'
            self.write(message)
            self.applyChanges()
            self.exitCommandMode()
        except CommunicationError as err:
            print("Error in setTxPowerLevel caused by: %s" %err)
            return 

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
        

    def transmitSerialData(self, data, address, stringData = True):
        frame = self.create16BitAddrFrame(data, address=address, mode=0, stringData=stringData)
        self.serialPort.write(frame)

    def transparentTransmit(self, data, address):
        if address == self.destAddr:
            pass
        else:
            self.setDL(address)
        self.serialPort.write(data)
        self.serialPort.flush()

    def transparentRead(self, packetSize=32):
        return self.serialPort.read(packetSize)




'''
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




def testTransparentMode():
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
            time.sleep(1.1)
            xbee.setMaxBaud()
            xbeeBaudRate = xbee.getBaudRate()
            print("Error resolved: Baud rate now set to 250000")
        else:
            print("error with xbee initial baud rate, exiting program")
    #Needs to 2 seoncds for radio to settle
    

    print("Xbee online @%s baud and addressed as %s" %(str(xbeeBaudRate).strip(), str(address).strip()))
    mode = input("(T)x or (R)x")
    if mode == "T":
        data = b''
        for i in range(0,250):
            data+=(bytes([i]))
        print("Entered transmitter mode: Transparent Mode operation")
        messageNum = 0
        while(messageNum < 1000):
            xbee.transparentTransmit(data)
            messageNum += 1

    else:
        data = []
        print("Entered Rx mode")
        startTime = 0
        while(len(data) < 1000):
            message = xbee.transparentRead(packetSize=250)
            if startTime == 0:
                startTime = time.time()
            if message:
                data.append(message)
                #print(len(data))

        endTime = time.time()

        print("Elapsed time: %s" %(endTime - startTime))







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
    time.sleep(1.1)
    xbee.setMy16BitAddress(sys.argv[3+incrementArgs])
    xbee.setDH16Addr()
    xbee.enableAPIMode()
    time.sleep(1.1)
    address = xbee.getMy16BitAddress()
    print("Xbee online @%s baud and addressed as %s" %(str(xbeeBaudRate).strip(), str(address).strip()))
    mode = input("(T)x or (R)x")
    if mode == "T":
        data = bytes([0])
        data = data*100
        print("Entered tranmitter mode")
        messageNum = 0
        while(messageNum < 1000):
            xbee.transmitSerialData(data, 0xBBBB, stringData=False)
            messageNum += 1
            time.sleep(0.01)
    else:
        data = []
        print("Entered Rx mode")
        startTime = 0
        while(len(data) < 1000):
            message = xbee.readSerialData()
            if startTime == 0:
                startTime = time.time()
            if message:
                data.append(message)
                print(len(data))
        endTime = time.time()

        print("Elapsed time: %s" %(endTime - startTime))
        

if __name__ == '__main__':
    testTransparentMode()

'''