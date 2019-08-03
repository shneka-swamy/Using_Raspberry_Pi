from digi.xbee.devices import *
from scipy.io import wavfile
import numpy as np
import string

def create_message(data):
	length = 0
	send_list = []
	string = ''
	i = 0

	for e in data:
		length += len(str(e)) + 1

		if i==0:
			string = str(e)
			i = 1

		elif length <=100:
			string = string +' '+str(e)

		else:
			send_list.append(string)
			del(string)
			length = len(str(e))
			string = str(e)

	if length != 0:
		send_list.append(string)

	return send_list


def send_message(send_list, alpha):

    device = XBeeDevice("/dev/ttyS0",115200)

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                   ("0013A2004102FC32"))

    device.open() 

    try:

    	for j in range(0, len(send_list)):
    	    device.send_data(remote_device, str(send_list[j]))

    	device.send_data(remote_device, str(alpha))

    	print("Waiting for final acknowledgement")

    	xbee_message = device.read_data()

    	while xbee_message is None:

    		xbee_message = device.read_data()

    	print("Entire data received")

    finally:
    	device.close()
    

def send_final_bit(fs):

    print("Entered")
    
    device = XBeeDevice("/dev/ttyS0", 115200)

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                   ("0013A2004102FC32"))

    device.open() 

    try:
        for j in range(0, 5):
            device.send_data(remote_device, str(fs))
            device.send_data(remote_device, str('f'))

        print("Waiting for final acknowledgement")

        xbee_message = device.read_data()

        while xbee_message is None:

            xbee_message = device.read_data()

        print("Entire data received")

    finally:
    	device.close()


def main():

    fs, data = wavfile.read('first.wav', 'b')

    print(data.size)


    send_list = create_message(data)

    alpha_limit = 0

    alpha = list(string.ascii_lowercase[0:26])


    # The number of packets here is chosen to be 1000 based on the experiments previously conducted
    # When the number of values is 1000 the packets are transferred without any loss.


    j = 0
    set_limit = 1000


    while j < len(send_list):
        #send_message(send_list[j:j+10], alpha[alpha_limit])
    	send_message(send_list[j:j+set_limit], alpha[alpha_limit])
    	j += set_limit
    	alpha_limit += 1

    send_final_bit(fs)


if __name__ == '__main__':
    main()
