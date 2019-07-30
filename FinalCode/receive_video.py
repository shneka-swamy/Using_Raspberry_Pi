from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np

# Need a method to stop collecting the data once the entire video is sent
# Can this be done using a check bit?

def convert_to_voice(received, fs_new):
    wavfile.write('new_first.wav', fs_new, received)

def receive_data(device, remote_device):
    try:
        device.open()
        list_val = []
        print("Waiting for data...\n")

        value = 0
        i = 0
        while value !=16000:
            xbee_message = device.read_data()

            if xbee_message is not None:
               string_val = xbee_message.data.decode().split()
               list_val += string_val
               #print(list_val)

               if len(string_val) == 1:
                   value = int(string_val[0])
               #print(value)

    finally:
        if device is not None and device.is_open():
            print("Entered")
            device.send_data(remote_device, "Received")
            print(len(list_val))
            received = np.asarray(list_val).astype(np.int16)
            fs_new = received[-1]
            received = received[:-1]
            device.close()

    convert_to_voice(received, fs_new)

def main():
    device = XBeeDevice("/dev/ttyS0", 115200)

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                     ("0013A2004102FC76"))
    received = receive_data(device, remote_device)


if __name__ == '__main__':
    main()
