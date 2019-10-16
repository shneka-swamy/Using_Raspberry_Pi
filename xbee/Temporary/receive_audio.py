import pyaudio
import wave
import sys
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *


#This is test code.

def receive(input_audio):
    pya = pyaudio.PyAudio()
    OUTPUT_SAMPLE_RATE = 44100
    stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)

    bytestream = input_audio
    stream.write(bytestream)
    stream.stop_stream()
    stream.close()

"""
# Communication from receiver node to sender node.
def transmit(data, remote_device, local_xbee):
    try:
        if (not local_xbee.is_open()):
            local_xbee.open()
        local_xbee.send_data(remote_device, data)

    except:
        print (local_xbee.log)
"""
#TODO: This must receive data, then send a confirmation of that data.
#It should likely also call another method to play back the data.

def data_rec(xbee_message):
    add_to_data(xbee_message)

def add_to_data(self, xbee_message):
    print(counter)
    #data.append(xbee_message.data)
    pass

def receive_audio(data, data_stream):
    data.append(data_stream)



def main():

    #Initializes the device.
    device = XBeeDevice("/dev/ttyS0", 250000)
    device.open()

    #Initializes the remote device.
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                     ("0013A2004102FC76"))
    
    data = []   
    counter = 1
    device.add_data_received_callback(data_rec)
    while(True):
        input
    device.close()

if __name__ == '__main__':
    main()
