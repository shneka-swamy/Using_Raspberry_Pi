
from XbeeModule import *

import time
import wave
import argparse
import pyaudio
import numpy as np
import scipy.signal as sps
from scipy.io import wavfile
import librosa
from threading import Thread
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *
import threading



def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description='audio player')

    parser = argparse.ArgumentParser(description='audio player')
    parser.add_argument('--addr', action='store', dest='address', type=str, help='16 bit address')
    parser.add_argument('--port', action='store', dest='portName', default='/dev/ttyUSB0')
    parser.add_argument('--rate', action='store', dest='baudRate', type=int, default=250000)
    parser.add_argument('--api', action='store', dest='apiMode', type=str2bool, default=False)
    parser.add_argument('--s1', action='store', dest='S1Mode', type=str2bool, default=False)
    args = parser.parse_args()

    xbee = Xbee(args.portName, args.baudRate, args.address, apiMode=args.apiMode, S1=args.S1Mode)
    address = ""
    
    def getAddress():
        try:
            return xbee.getMy16BitAddress()
        except CommunicationException as err:
            time.sleep(2)
            getAddress()

    

    print(f"Online @ {getAddress()}")

    

    mode = input("(T)x or (R)x")

    

    FORMAT = 8
    CHANNELS = 1
    RATE = 8000
    CHUNK=512
    RECORD_SECONDS = 30
  

   
    
    if mode == "T":
        
        audio_file = '../AudioFiles/StarWars60_8kHz.wav'
        wf = wave.open(audio_file, 'rb')

        p = pyaudio.PyAudio()
        #print(f"sample rate {s}")
        print(f"width {p.get_format_from_width(wf.getsampwidth())}")
        print(f"channels {wf.getnchannels()}")
        print(f"framerate {wf.getframerate()}")

        
        #Stream creates a stream of audio data that can be transmitted as a series of strings.
        
        outStream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

        song = []
        
        data = wf.readframes(CHUNK)
        while len(data) > 0:
            song.append(data)
            data = wf.readframes(CHUNK)
        
        outStream.stop_stream()
        outStream.close()    

        messageNum = 1
        for packet in song:
            xbee.transmit(packet, "BBBB")
            print(f"{messageNum}  {len(packet)}")
            messageNum += 1


        # close PyAudio 
        p.terminate()

        

    else:

        audio = pyaudio.PyAudio()
        

        def callback(in_data, frame_count, time_info, status):
            stream.write(frames)
            return (frames, pyaudio.paContinue)
 
        # start Recording
        
        stream = audio.open(format=FORMAT, 
                        channels=CHANNELS,
                        rate=RATE, 
                        output=True)
        
        
        data = b''
        startTime = time.time()
        print("Entered Rx mode")
        messageNum = 0
        activeTransmission = False
        frames = b''

        def playAudio(audioClip):
            stream.write(audioClip)

            

        while activeTransmission or messageNum == 0:
            data = xbee.read(packetSize=CHUNK*2)
            if len(data) != 0 and messageNum == 0:
                activeTransmission = True
            elif activeTransmission and len(data) == 0:
                activeTransmission = False
                break
            elif len(data) == 0: continue
            if activeTransmission:
                if len(frames) > RATE:
                    t = Thread(target=playAudio, args=(frames,))
                    t.start()
                    frames = b''
            frames += data
            messageNum+=1
            
            print(f"{messageNum}  {len(frames)}")
        print ("finished recording")



        endTime = time.time()
        print("Elapsed time: %s" %(endTime - startTime))
        print(f"total size {len(frames)*len(data)}")
        print(f"data rate achieved {(len(frames)*len(data))/ (endTime - startTime) * 8 / 1000}")

        stream.close()
        audio.terminate()

        
   


if __name__ == '__main__':
    main()