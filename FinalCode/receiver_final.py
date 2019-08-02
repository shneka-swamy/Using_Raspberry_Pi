from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np

# Need a method to stop collecting the data once the entire video is sent
# Can this be done using a check bit?

def convert_to_voice(received, fs_new):
    wavfile.write('new_first.wav', fs_new, received)

def receive_data(device, remote_device, new_list):
    
    device.open()

    try:
        list_val = []
        print("Waiting for data...\n")

        flag = True

        while flag:
            xbee_message = device.read_data()

            if xbee_message is not None:
               string_val = xbee_message.data.decode().split()
               list_val += string_val

               if len(string_val) == 1 && string_val.is_alpha():
                flag = False
                

    finally:
        if device is not None and device.is_open():
            print("Entered")

            print(len(list_val))
            new_list.append(list_val[:-1])
            device.send_data(remote_device, "Received")
            
            device.close()

    return new_list

def main():
    new_list = []

    device = XBeeDevice("/dev/ttyS0", 115200)

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                     ("0013A2004102FC76"))
    
    open_flag = True

    while open_flag:
        new_list = receive_data(device, remote_device, new_list)
        if new_list[-1] == 'f':
            open_flag = False

    print(len(new_list))


if __name__ == '__main__':
    main()