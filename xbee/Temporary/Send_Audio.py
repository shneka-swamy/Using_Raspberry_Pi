import pyaudio
import wave
import sys
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *

import receive_audio

pya = pyaudio.PyAudio()
OUTPUT_SAMPLE_RATE = 44100
stream2 = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)


print ("Starting program")
# Instantiate an XBee device object.
local_xbee = XBeeDevice("COM5", 9600)
local_xbee.set_sync_ops_timeout(1)
remote_device = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string
                                                ("0013A2004102FC76"))

# Open the device connection.

def transmit(data):
    try:
        local_xbee.open()
        local_xbee.send_data_async(remote_device, data) 

    except:
        local_xbee.open()
        print (local_xbee.log)

    finally:
        
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()


def hello():
    print ("Hello World!")

def send_audio(chunk_size, audio_file):

    CHUNK = chunk_size


    print(sys.argv)

    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        #sys.exit(-1)

    #wf is the wave file to be played.
    wf = wave.open(audio_file, 'rb')

    #p is the audio player.
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    
    data = wf.readframes(CHUNK)

    while data != '':
        #stream.write(data)
        data = wf.readframes(CHUNK)

        transmit(str(data))

        #Simulation for data received by the receiver.
        #receive_audio.receive(data)




    stream.stop_stream()
    stream.close()

    p.terminate()



def receive(input_audio):

        bytestream = input_audio
        stream2.write(bytestream)
        stream2.stop_stream()
        stream2.close()