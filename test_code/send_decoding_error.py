# Send Video to another xbee

from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np
import time

def send_message(device, remote_device, data, i, limit):
    # Limit is the number of packets that must be sent 
    # i is the initial value to run the loop

    length = 0
    send_list = []
    string = ''
    value = 0

    for e in data:
        if value < limit - 1:
            length += len(str(e)) + 1

            if i==0:
                string = str(e)
                i = 1

            elif length <=100:
                string = string +' '+str(e)

            else:
                send_list.append(string)
                del(string)
                length = len(str(e))
                string = str(e)
            value = len(send_list)
            
    if length != 0:
        send_list.append(string)
     
    print(len(send_list))
    
    for j in range(0, len(send_list)):
        device.send_data(remote_device, str(send_list[j]))
    
   

def main():
    device = XBeeDevice("/dev/ttyS0",115200)

    fs, data = wavfile.read('first.wav', 'b')

    print(data.size)

    device.open() 
    
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                    ("0013A2004102FC32"))


    send_message(device, remote_device, data, 0,2000)

    for e in range(0,10):
        device.send_data(remote_device, str(fs))

    try:
        print("Waiting for final acknowledgement")

        xbee_message = device.read_data()

        while xbee_message is None:
            xbee_message = device.read_data()

        print("Entier data received")

    finally:
        device.close()
        


if __name__ == '__main__':
    main()
