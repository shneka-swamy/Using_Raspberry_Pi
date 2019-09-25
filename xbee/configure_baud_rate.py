import serial
import time

class Xbee_Configuration:
    def __init__(self, port_name='/dev/ttyUSB0', baud_rate=115200, timeout=1):
        self.ser = serial.Serial(port_name, baud_rate, timeout=timeout)


    def set_comm_baud_rate(self, baud_rate):
        self.ser.baudrate = baud_rate

    def close(self):
        self.ser.close()

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

        self.ser.write(b'ATCN\r')

        return True
    
    
    def send_tx_data(self):
        self.ser.write(b'this is a test')

def main():
    xbee = Xbee_Configuration()
    if xbee.set_xbee_max_baud():
        print("set max baud")
        xbee.set_comm_baud_rate(250000)
        time.sleep(1)

    xbee.send_tx_data()

if __name__ == '__main__':
    main()

    
