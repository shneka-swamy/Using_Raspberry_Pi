# Send Video to another xbee

from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np
import time

def send_message(device, remote_device, data, i, limit):

    set_base = 10
    send_list = []
    while (i+1)*set_base <= limit:
        send_list.append(' '.join(str(e) for e in data[(i*set_base):((i+1)*set_base)]))
        i+=1

    print(len(send_list))    

    for j in range(0,len(send_list)):
        device.send_data(remote_device,send_list[j])

    del send_list[:] 

def main():
    device = XBeeDevice("/dev/ttyS0",115200)

    fs, data = wavfile.read('first.wav', 'b')

    print(data.size)
    
    # Have to send the value of fs.
    # Is there an efficient way to do this ?
    # Dont set the base chang  it to accomodata the most plausible length of the string
    
    device.open() 
    
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                ("0013A2004102FC32"))


    # Call the function to send messages
    send_message(device, remote_device, data, 0, 30000)

    #time.sleep(10)
    #send_message(device, remote_device, data, 1000, 20000)
    #time.sleep(10)
    #send_message(device, remote_device, data, 2000, 30000)
    #time.sleep(10)
    #send_message(device, remote_device, data, 3000, 40000)
    #time.sleep(15)
    #send_message(device, remote_device, data, 4000, 50000)
    
    # This is the last value that must be sent.
    # The receiving of this value must shut the program
    for e in range(0,5):
        device.send_data(remote_device, str(fs))

    try:
        print("Waiting for final acknowledgement")

        xbee_message = device.read_data()

        while xbee_message is None:
            xbee_message = device.read_data()

        print("Entire data received")

    finally:
        device.close()
        


if __name__ == '__main__':
    main()
