import pyaudio
import wave
import sys
from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.exception import *
import numpy as np

#This is test code.
class receiver:

	def __init__(self):
		self.data = bytearray()
		self.counter=1

	def playAudio(self):
		self.data = np.array(self.data, dtype=np.float32)
		pya = pyaudio.PyAudio()
		OUTPUT_SAMPLE_RATE = 44100
		stream = pya.open(format=pya.get_format_from_width(1), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)

		self.data = self.data.astype(np.float32).tostring()
		print (len(self.data))
		stream.write(self.data)
		stream.stop_stream()
		stream.close()


	def data_rec(self,xbee_message):
		#Add function to play audio
		#if xbee_message.data == ""
		#self.data.append(xbee_message.data)
		self.data += xbee_message.data
		# print (xbee_message.data)
		if (self.counter%10==0):
			print(self.counter)
		self.counter+=1
		if self.counter == 1322:
			self.playAudio()





def main():

		#Initializes the device.
		device = XBeeDevice("/dev/ttyS0", 250000)
		device.open()

		#Initializes the remote device.
		remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
									 ("0013A2004102FC76"))
		rec = receiver()

#		device.add_data_received_callback(rec.data_rec)

		while(True):
			xbee_message = device.read_data()
			if xbee_message:
				rec.counter += 1
				print(rec.counter)
		device.close()

if __name__ == '__main__':
    main()
