from digi.xbee.devices import *

# Edit the code for multiple destiantions (can be implemented later)


class RouteFormation:

	# The route request uses the following message pattern to set up communication
	# Source Request is < Broadcast ID, Sequence Number , Hop Number, Degree, Source ID, Intermediate ID , Destination ID (number can vary)>
	# Route Reply is of the form <Sequence Number, Broadcast ID, Hop Number, Source, Intermediate >
	def __init__(self):
		self.rreq = ""
		self.isSource = False
		self.SeqenceNo = 0
		self.Id = 0
		self.destination = []
		self.table = []
		self.inter_table = []
		self.rem = []
		self.neighbourcount = 0
		self.rrep = ""

	# <Sequence Number, Hop number, Degree, Source ID, Intermediate ID, Destination ID, Expiry Time>
	def createTable(self, device):
		print("Entered")
		self.device_discovery(device)
		self.neighbourcount = len(self.rem)
			
		if self.neighbourcount == 0:
			print("No neighbour found so far try after sometime")
		else:
			for i in range(0, self.neighbourcount):
				self.table.append([str(self.SeqenceNo), str(1), str(self.neighbourcount), str(device.get_64bit_addr()),self.rem[i],self.rem[i], 5])
		
		print(self.table) 

	# <Sequence Number,Hop Number, Degree, Source ID, Intermediate ID, Destiantion ID, Expiry>
	def updateTable_reply(self, message):
		
		for block in self.table:
			
			# Don't make any changes if the time for keeping the block expires
			if block[-1] == 0:
				self.table.remove(block)
			# If the destination is the same 
			# This happens when the sequence number is greater or the hop number is lower
			else:
				if message[5] == block[5] and (int(block[0]) < int(message[0]) or int(block[1])  > int(message[1])):
					block[:] = message[0:6] 
					block.append(5)
		print("Table Updated at Reply:")
		print(self.table)

	# Must check the logic behind this part 
	def updateTable_request(self, device, message):
		for block in self.table:
			
			if block[-1] == 0:
				self.table.remove(block)
			# If the destiantion needs to be chaged
			# This happens when the sequence number is greater or the block number is lower
			else:
				if message[4] == block[5] and (int(block[0]) <  int(message[1]) or int(block[1]) > int(message[2])):
					print("Actually updating table")
					block[:] = message[1:4]
					block.append(str(device.get_64bit_addr()))
					block.append(message[5])
					block.append(message[4])
					block.append(5)

		print("Table Updated at Request:")
		print(self.table)


	def generateRREQ(self, device, dest):
		
		degree = self.neighbourcount

		self.rreq += str(self.Id) + ' ' + str(self.SeqenceNo) + ' ' + str(1) + ' ' + str(degree) + ' '
		self.rreq += str(device.get_64bit_addr()) + ' ' + str(device.get_64bit_addr()) + ' '
		self.rreq += dest
		#print("<Sequence Number, Broadcast ID, Hop Number, Degree, Source ID, InterSource, Destintion ID>")
		#print(self.rreq)
		
		# Drop the packet when duplicated and when multiple path request are made at the same time.
		self.interTable(self.rreq.split())
		# Every message sent will increase the sequence number
		self.SeqenceNo += 1
		device.send_data_broadcast(self.rreq)

		self.sendReply(device)
		
	def declareSource(self, device, dest):
		self.isSource = True
		self.generateRREQ(device, dest)


	# Code that discovers other devices in the network 
	# Discovers itself and other devices in range with the same baud rate.
	def device_discovery(self, device):
		xbee_net = device.get_network()
		xbee_net.set_discovery_timeout(15)
		xbee_net.clear()

		def callback_device_discovered(remote):
			print("Device discovered is %s" %remote)
			self.rem.append(str(remote).split()[0])

		def callback_discovery_finished(status):
			if status == NetworkDiscoveryStatus.SUCCESS:
				print("Discovery process finished successfully")
			else:
				print("Discovery process not successful")

		xbee_net.add_device_discovered_callback(callback_device_discovered)
		xbee_net.add_discovery_process_finished_callback(callback_discovery_finished)
		xbee_net.start_discovery_process()

		print("Discovering Remote XBee Devices.")

		while xbee_net.is_discovery_running():
			time.sleep(0.1)

	# This table can be used to get back to the source (must not be dropped)
	def interTable(self, message):
		# Consist of the information in the received queue 
		# Essentially requires only braodcast Id and source. (Other details are stored for possible optimisation)
		self.inter_table.append(message)
		print("Intermediate  Table :")
		print(self.inter_table)


	def generateRREP(self, device, remote_device,  message):
		degree = self.neighbourcount

		self.rrep += str(self.SeqenceNo) + ' ' + message[2] + ' ' + str(degree + int(message[3])) + ' '
		self.rrep += message[4] + ' ' + str(device.get_64bit_addr()) + ' '
		self.rrep += message[6]

		device.send_data(remote_device, self.rrep)

	# Use a call back function instead ??		
	def sendReply(self, device):

		print("Waiting for data...\n")
		flag = True

		while flag:
			xbee_message = device.read_data()

			if xbee_message is not None:
				string_val = xbee_message.data.decode().split()
				print(string_val)

				# Helps identify the Route Request Packet
				# Once a request is got run a timer (must be added later)
				if len(string_val) == 7:
					duplicate_flag = False
						
					# This condition checks if the same message request is reaching the node. 
					# The value 0 can be changed after the intermediate node is formed.
					for list in self.inter_table:
						if list[4] == string_val[4] and list[0] == string_val[0]:
							print("Drop the message, extra information received")
							duplicate_flag = True
							break 

					if duplicate_flag == False:

						self.interTable(string_val)
						if str(device.get_64bit_addr()) == string_val[6]:
							remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string (string_val[5]))
							self.SeqenceNo += 1
							# Add the source as destianation to the table
							self.updateTable_request(device, string_val)

							# The timer is used to set the path to wait for sometime to get the path 
							start = time.time()
							while(time.time() - start < 5):
								pass

							self.generateRREP(device, remote_device, string_val)
						else:
							print("wait")
							self.interTable(string_val)
							self.updateTable_request(device, string_val)
							self.SeqenceNo += 1
							string_val[5] = str(device.get_64bit_addr())
							string_val[3] = str(int(string_val[3]) + self.neighbourcount)
							string_val[2] = str(int(string_val[2]) + 1)
							device.send_data_broadcast(' '.join(string_val))


				# When the value of the message received is 6 a reply message is received.
				# Look at the intermediate table and send the message through the intermediate node.
				if len(string_val) == 6:
					print("Processing Reply:")
					path_flag = True

					print(string_val)

					for member in self.inter_table:
						print("Check the graph")
						print(member[6])
						print(member[4])
						if member[6] == string_val[5] and member[4] == string_val[3]: 
							self.updateTable_reply(string_val)
							path_flag = False

					if path_flag == True:
						print("Error. Wrong reply received, node not in path")
					else:
						if str(device.get_64bit_addr()) == string_val[3]:
							remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string (string_val[4]))
							# To get the route while sending a data, the table must be verified
							print("Send Message - Path is set")
						# If the source is not reached  send the information forward.
						else:
							print("What ??")
							remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(string_val[4]))
							#device.send_data(remote_device,' '.join(string_val))	
							print("Forward not the path")

def main():

	# To open the Xbee device and to work with it
	device = XBeeDevice("/dev/ttyUSB3", 250000)
	device.open()

	# Create an object for sending Route Request for a message
	# In the beginning of the program - do the following 
	rreq = RouteFormation()
	rreq.createTable(device)

	# This function must be called when not set as a source
	rreq.sendReply(device)

	# These steps are inherent to source node.
	# print ("Press 'y' to declare as the source")	

	#rreq.declareSource(device, "0013A20040B317F6")
	#rreq.declareSource(device, "0013A2004102FC76")
	#rreq.declareSource(device, "0013A20040B317F6")
	#rreq.declareSource(device, "0013A2004102FC76")


	device.close()

if __name__ == "__main__":
	main()

