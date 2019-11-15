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

    parser.add_argument('--addr', action='store', dest='address', type=str, help='16 bit address')
    parser.add_argument('--port', action='store', dest='portName', default='/dev/ttyUSB0')
    parser.add_argument('--rate', action='store', dest='baudRate', type=int, default=250000)
    parser.add_argument('--api', action='store', dest='apiMode', type=str2bool, default=True)
    args = parser.parse_args()

    print(args.apiMode)
    xbee = Xbee(args.portName, args.baudRate, args.address, args.apiMode)
   
    if args.apiMode:
        xbee_interface = Raw802Device(args.portName, 250000)


        xbee_interface.open()

    

        protocol = xbee_interface.get_protocol()
        print(xbee_interface.get_64bit_addr())
        print(protocol)
        #xbee_interface.set_16bit_addr(XBee16BitAddress.from_hex_string(args.address))
        #localAddress = xbee_interface.get_16bit_addr()
        if args.address == 'AAAA':
            remote_device = RemoteXBeeDevice(xbee_interface, XBee64BitAddress.from_hex_string("0013A200419B5611"))
        else:
            remote_device = RemoteXBeeDevice(xbee_interface, XBee64BitAddress.from_hex_string("0013A200419B5625"))

        choice = input('Rx or Tx')





        if choice == 'r':
            
            #device.add_data_received_callback(rec.data_rec)
            messages = []
            while(True):
                xbee_message = xbee_interface.read_data()
                if xbee_message:
                        messages.append(xbee_message)
                        if len(messages) % 10 == 0:
                            print(len(messages))

        else:
            for x in range (0, 255):
                arr = bytearray([x]*100)
                if x % 10 == 0:
                    print(x, "SyncMessage")
                    xbee_interface.send_data(remote_device, arr)
                else:
                    xbee_interface.send_data(remote_device, arr)

        
        
        xbee_interface.close()

    else:
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
    
    



    mode = input("(T)x or (R)x")
    if mode == "T":
        audio_file = '../AudioFiles/PinkPanther30.wav'
        CHUNK=100
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
        #datda = scipy.signal.resample(data, 8000)
        print(len(data))
        while len(data) > 0:
            xbee.transparentTransmit(data, remote_device[8:])
            print(messageNum)
            messageNum += 1
            data = wf.readframes(CHUNK)
        
        # stop stream 
        stream.stop_stream()
        stream.close()

        # close PyAudio 
        p.terminate()
        

    else:

       

        data = b''
        print("Entered Rx mode")
        startTime = 0
        while(len(data) < 1310000):
            message = xbee.transparentRead(packetSize=200)
            if startTime == 0:
                startTime = time.time()
            if message:
                data += message
                print(len(data))

        endTime = time.time()
        print("Elapsed time: %s" %(endTime - startTime))

        
        
        
        
        audio_file = '../AudioFiles/CantinaBand3.wav'
        CHUNK=100
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

        
   


if __name__ == '__main__':
    main()