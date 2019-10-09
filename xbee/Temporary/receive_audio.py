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


# Communication from receiver node to sender node.
def transmit(data, remote_device, local_xbee):
    try:
        if (not local_xbee.is_open()):
            local_xbee.open()
        local_xbee.send_data(remote_device, data)

    except:
        print (local_xbee.log)

#TODO: This must receive data, then send a confirmation of that data.
#It should likely also call another method to play back the data.
def receive_audio(local_device, remote_device, data_stream):
    if (not data_stream == None):
        print (data_stream)
    #Send a reponse message 20 times.
    for x in range (0, 20):
        transmit('c', remote_device, local_device)



def main():

    #Initializes the device.
    device = XBeeDevice("COM4", 57600)
    device.open()

    #Initializes the remote device.
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                     ("0013A2004102FC76"))

    #Grabs an initial piece of data.
    data_stream = device.read_data()

    #Reads data until silence occurs.
    while (data_stream != ''):
        receive_audio(device, remote_device, data_stream)
        data_stream = device.read_data()

    device.close()

if __name__ == '__main__':
    main()
