import pyaudio
import wave
import sys
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *

import receive_audio
import numpy as np

print ("Starting program")
# Instantiate an XBee device object.
local_xbee = XBeeDevice("/dev/ttyS0", 250000)
#local_xbee.set_sync_ops_timeout(1)
remote_device = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string
                                                ("0013A2004102FC32"))

# Open the device connection.

def transmit(data):
    try:
        #Opens serial communication with the xbee.
        #local_xbee.open()

        #Sends data asyncronously (remove _async for sync mode)
        local_xbee.send_data(remote_device, data) 

        '''
        response = local_xbee.read_data()
        while (response == None):
            response = local_xbee.read_data()
    
        print ("Received Response: ")
        '''

    except:
        #Designed to open, then close the port.
        #local_xbee.open()
        print (local_xbee.log)

    #Designed for closing ports.
    '''
    finally:
        
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()

    '''

def send_audio(chunk_size, audio_file):

    CHUNK = chunk_size

    #Built in functionality from pyAudio.
    '''
    print(sys.argv)

    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        #sys.exit(-1)
    '''

    #wf is the wave file to be played.
    wf = wave.open(audio_file, 'rb')

    #p is the audio player.
    p = pyaudio.PyAudio()
    #Stream creates a stream of audio data that can be transmitted as a series of strings.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)


    '''
    f = open('../examples.csv')

    while True:
        line = f.readline()
        if not line:
            break

        transmit(line)

    '''
    array = []
    #Grabs the first chunk of data.
    data = wf.readframes(CHUNK)
    counter=0
    #Reads data until there is silence from the audio file.
    while data:
        #stream.write(data)
        array.append(data)
        counter+=1
        print(counter,"*")
        data = wf.readframes(CHUNK)
    

    """Test audio """
    """
    data = np.array(data, dtype=np.float32)
    data= data.astype(np.float32).tostring()
    pya = pyaudio.PyAudio()
    stream = pya.open(format=pya.get_format_from_width(1), channels=1,rate=44100, output=True)

    
    stream.write(data)
    stream.stop_stream()
    stream.close()
    """ 

        #Calls the transmit function and passes in a string of data the size of chunk.
    for x in range (0, len(array)):
        if x % 100 == 0:
            local_xbee.send_data(remote_device, array[x])
        else:
            local_xbee.send_data_async(remote_device, array[x])
        if x >= 1141 and x  <= 1152:
            print(array[x])
        #print(x)
        #Simulation for data received by the receiver.
        #receive_audio.receive(data)



    stream.stop_stream()
    stream.close()
    print("Done")
    p.terminate()
    local_xbee.close()
    exit()

def main():
    #One time open of the xbee instead of opening and closing the xbee.
    local_xbee.open()
    send_audio(50, "../../AudioFiles/CantinaBand3.wav")
    

if __name__ == '__main__':
    main()
