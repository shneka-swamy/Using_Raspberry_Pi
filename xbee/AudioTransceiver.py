from XbeeModule import Xbee


import wave
import argparse
import pyaudio
import scipy
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *



def audioTest():
    audio_file = '../AudioFiles/CantinaBand3.wav'
    CHUNK=100
    wf = wave.open(audio_file, 'rb')

    p = pyaudio.PyAudio()
    #Stream creates a stream of audio data that can be transmitted as a series of strings.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    data = wf.readframes(CHUNK)
    messageNum = 1
    print(data)
    while len(data) > 0:
        #print(messageNum)
        messageNum += 1
        stream.write(data)
        data = wf.readframes(CHUNK)

    print(messageNum)
    # stop stream 
    stream.stop_stream()
    stream.close()

    # close PyAudio 
    p.terminate()


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

    xbee = Xbee(args.portName, args.baudRate, args.address, args.apiMode, args.S1Mode)
   

    address = xbee.getMy16BitAddress()
    print(f"Online @ {address}")
    
    if args.address == 'AAAA':
        #remote_device ="0013A200419B5611"
        remote_device = "000000000000BBBB"

        xbee.setDH(remote_device[0:8])
        xbee.setDL(remote_device[8:])

    else:
        remote_device = "000000000000AAAA"
        xbee.setDH(remote_device[0:8])
        xbee.setDL(remote_device[8:])

    

    CHUNK=15

    mode = input("(T)x or (R)x")

    data = [i for i in range(CHUNK)]
    data  = bytes(data)
    

    if mode == "T":
        '''
        audio_file = '../AudioFiles/CantinaBand3.wav'
        wf = wave.open(audio_file, 'rb')

        p = pyaudio.PyAudio()
        #Stream creates a stream of audio data that can be transmitted as a series of strings.
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
        
        messageNum = 1
        data = wf.readframes(CHUNK)
        print(len(data))
        #data = scipy.signal.resample(data, 8000)
        while len(data) > 0:
            xbee.transparentTransmit(data, remote_device[8:])
            print(messageNum)
            messageNum += 1
            data = wf.readframes(CHUNK)
        time.sleep(2.5)
        xbee.transparentTransmit(b'END', remote_device[8:])

        # stop stream 
        stream.stop_stream()
        stream.close()

        # close PyAudio 
        p.terminate()
        '''
        for repeats in range(1000):
            xbee.transparentTransmit(data, remote_device[8:])
            print(repeats)
        xbee.transparentTransmit(b'END', remote_device[8:])
        

    else:

       

        data = b''
        print("Entered Rx mode")
        messageNum = 0
        startTime = 0
        while(True):
            messageNum+=1
            message = xbee.transparentRead(packetSize=CHUNK)
            if startTime == 0:
                startTime = time.time()
            if message:
                if message == b'END':
                    break
                if len(message) != CHUNK:
                    print(f"error with message {messageNum}")
                print(messageNum)
                data += message


        endTime = time.time()
        print("Elapsed time: %s" %(endTime - startTime))
        print(len(data))
        print(f"data rate achieved {len(data)/ (endTime - startTime) * 8 / 1000}")

        
        
        '''
        audio_file = '../AudioFiles/CantinaBand3.wav'
        wf = wave.open(audio_file, 'rb')

        p = pyaudio.PyAudio()
        #Stream creates a stream of audio data that can be transmitted as a series of strings.
        stream = stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)


        stream.write(data)



        # stop stream 
        stream.stop_stream()
        stream.close()

        # close PyAudio 
        p.terminate()

        '''
   


if __name__ == '__main__':
    main()