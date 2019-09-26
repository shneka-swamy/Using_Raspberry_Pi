import serial
import time

class Xbee_Configuration:
    def __init__(self, port_name='/dev/ttyUSB0', baud_rate=115200, timeout=1):
        with serial.Serial(port_name, baud_rate, timeout=timeout) as self.ser:
            print(self.ser)        

    def set_comm_baud_rate(self, baud_rate):
        self.ser.baudrate = baud_rate
        print("Communication baud rate set to %s" % self.ser.baudrate)


    def verify_response(self, time_delay):
        time.sleep(time_delay)
        line = self.ser.readline()
        print(line)
        return b'OK' in line

    def set_xbee_max_baud(self):
        self.ser.write(b'+++')
        
        if not self.verify_response(2):
            return False

        self.ser.write(b'ATWR\r')
        if not self.verify_response(.5):
            return False

        self.ser.write(b'ATBD3D090\r')
        if not self.verify_response(.5):
            return False

        self.ser.write(b'ATAC\r')
        if not self.verify_response(.5):
            return False 

        self.ser.write(b'ATCN\r')

        return True
    
    
    def enable_api_mode(self):
        self.ser.write(b'+++')
        if not self.verify_response(3):
            return False 

        self.ser.write(b'ATAP2\r')
        if not self.verify_response(.5):
            return False 
        self.ser.write(b'ATAC\r')
        if not self.verify_response(.5):
            return False 
        self.ser.write(b'ATCN\r')

        return True        


def main():
    xbee = Xbee_Configuration(port_name='/dev/ttyS0')
    if xbee.set_xbee_max_baud():
        print("set max baud")
        xbee.set_comm_baud_rate(250000)
        time.sleep(5)

    if xbee.enable_api_mode():
        print('Entered API Mode')
    else:
        print("Failed to enter API mode")
    xbee.close()

if __name__ == '__main__':
    main()

    
