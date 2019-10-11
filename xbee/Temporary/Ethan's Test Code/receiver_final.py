from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np
from pyAudio import *

# Need a method to stop collecting the data once the entire video is sent
# Can this be done using a check bit?

def convert_to_voice(received, fs_new):
    wavfile.write('new_first.wav', fs_new, received)

def receive_data(device, remote_device, new_list):

    try:
        list_val = []
        print("Waiting for data...\n")

        flag = True

        while flag:
            xbee_message = device.read_data()

            if xbee_message is not None:
               string_val = xbee_message.data.decode().split()
               list_val += string_val

               if len(string_val) == 1:
                   if string_val[0].isalpha():
                        flag = False
                

    finally:
        if device is not None and device.is_open():
            print("Entered")
            print(len(list_val))
            new_list += list_val
            device.send_data(remote_device, "Received")
        

    return new_list

def main():
    new_list = []

    device = XBeeDevice("/dev/ttyS0", 250000)

    device.open()

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                     ("0013A2004102FC76"))
    
    '''
    open_flag = True

    while open_flag:
        new_list = receive_data(device, remote_device, new_list)
        print(new_list[-1])
        if new_list[-1] == 'f':
            open_flag = False
        new_list = new_list[:-1]

    print(len(new_list))
    '''

    device.close()

if __name__ == '__main__':
    main()
