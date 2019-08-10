# This is an implementation of ADPCM encoder.
# This code is written in reference to Microchip code


# This file contains the global variables used in the program
import globval as gv
from scipy.io import wavfile

converted_file = []

# The list received is of order prevsample, previndex, code
def send_sample_encoder(check_list):
	final_file = [check_list[0]]
	send_list = [check_list[0], 0, 0]

	for i in range(1, len(check_list)):
		send_list = ADPCM_encoder(check_list[i], send_list)
		#print(send_list)
		final_file.append(send_list[2])

	return final_file

def inverse_quantizer(code, step):
	# Inverse quantize the ADPCM code into predicted difference using the quantizer
	# step size
	diffq = step >> 3
	if code & 4:
		diffq += step
	if code & 2:
		diffq += step >> 1
	if code & 1:
		diffq += step >> 2

	return diffq

def get_predicted_value(predsample, code, diffq):
	# Find the new predicted value by adding or subtracting the diffq
	if code & 8:
		predsample -= diffq
	else:
		predsample += diffq

	# Checking overflow
	if predsample > 32767:
		predsample = 32767
	elif predsample < -32768:
		predsample = -32768

	return predsample

def get_index_value(index, code):
	# Find the new stepsize and index value
	index += gv.IndexTable[code]
	if index < 0:
		index = 0
	if index > 88:
		index = 88
	
	return index


def ADPCM_encoder(sample, send_list):
	
	# To get the previous values set as a variable
	predsample = send_list[0]
	index = send_list[1]
	step = gv.StepSizeTable[index]

	# Compute the difference between actual and predicted sample
	diff = sample - predsample

	if diff >= 0:
		code = 0
	else:
		code = 8
		diff = -diff
	
	# Quantize the difference into 4 bit ADPCM code using the quanitzer step size
	tempstep = step
	if diff >= tempstep:
		code |= 4
		diff -= tempstep
	
	tempstep >>= 1
	if diff >= tempstep:
		code |= 2
		diff -= tempstep

	tempstep >>= 1
	if diff >= tempstep:
		code |= 1

	diffq = inverse_quantizer(code, step)
	predsample = get_predicted_value(predsample, code, diffq)
	index = get_index_value(index, code)

	send_list = [predsample, index, (code & 0x0f)]

	return send_list

def send_sample_decoder(check_list):
	original_file = [check_list[0]]
	received_list = [check_list[0], 0]
	#print(received_list)

	for i in range(1, len(check_list)):
		received_list = ADPCM_decoder(check_list[i], received_list)
		#print(received_list)
		original_file.append(received_list[0])

	return original_file


def ADPCM_decoder(code, send_list):
	predsample = send_list[0]
	index = send_list[1]

	step = gv.StepSizeTable[index]

	diffq = inverse_quantizer(code, step)
	predsample = get_predicted_value(predsample, code, diffq)
	index = get_index_value(index, code)

	send_list = [predsample, index]

	return send_list


def main():
	
	#fs, data = wavfile.read('first.wav', 'b')
	
	#print(data.size)
	
	check_list = [150, 155, 167, 170, 250, 250, 250, 250, 200]

	#check_list = [150, 155]

	converted_file = send_sample_encoder(check_list)
	print(converted_file)

	original_file = send_sample_decoder(converted_file)
	print(original_file)



if __name__ == '__main__':
	main()