
# This is the program written to enable routing
# The program assumes that the source and the receivers are known
# The source and destination will always have [0,0,0,0,1]

# Multiple sources can be set.. How to set multiple sinks ?
# Make the destination a list of lists ?


import graph as gp

class Nodes:
	"""docstring for ClassName"""

	def __init__(self, arg):
		# The message list considers the required message
		# [source, destination, Effective Degree, Hop, Mode of the Node]  
		# The modes of the nodes are defined as 0: Relay, 1: Source and 2: Destination
		# The message list also contains the nearby neighbours
		# The elements in the adj list (are appended when the member is visited)
		self.message_list = [arg]*5
	
	def set_source_dest(self, source, dest):
		self.message_list[0] = source
		self.message_list[1] = dest

	def change_value(self, source, hop):
		self.message_list[2] = len(gp.adj_list[source])
		self.message_list[3] = hop

	def append_neighbours(self, source):
		self.message_list += gp.adj_list[source]

	def erase_list(self, source):
		self.message_list = self.message_list[0:4]

# Path is the list that contains all the paths
# node is the element adjacent to the list
def get_path(path, node, NodeList):
	create_path = [(gp.destination, 0)]
	dest = gp.destination
	
	while dest != gp.source:
		create_path.append((NodeList[dest].message_list[0], NodeList[dest].message_list[2]))
		dest = NodeList[dest].message_list[0]

	path.append(create_path)


def main():

	# This function creates a node for each xbee system
	# The presence of a connection is depicted by the presence of an edge in the graph
	NodeList = []
	for i in range(0,10):
		NodeList.append(Nodes(0))

	# Setting value for the basic xbee
	# The value of source will always be -1
	
	stack = [gp.source]

	# To assign oneself as source or destination
	NodeList[gp.source].message_list[4] = 1
	NodeList[gp.destination] .message_list[4] = 2

	source_include = 3
	NodeList[source_include].message_list[4] = 1

	source_include = 5
	NodeList[source_include].message_list[4] = 1

	distances = []
	path = []

	while len(stack) != 0:
		# The stack contains the neighbours that must be looked at
		# A copy of this is maintained for computation purpose
		copy_stack = stack.copy()
		del stack[:]
		print(copy_stack)

		for node in copy_stack:
			if gp.destination in gp.adj_list[node]:
				NodeList[gp.destination].set_source_dest(node, gp.destination)
				NodeList[gp.destination].change_value(node, NodeList[node].message_list[3] + 1)
				distances.append(NodeList[node].message_list[3] + 1)
				print("In the path finding")
				get_path(path, node, NodeList)
				print(path)
			
			else:
				if node == gp.source:
					# Broadcast the message to all elements in te adj list
					for member in gp.adj_list[node]:
						if NodeList[member].message_list[4]!=1:
							NodeList[member].set_source_dest(node, gp.destination)
							NodeList[member].change_value(node, NodeList[node].message_list[3] + 1)
							NodeList[member].append_neighbours(node)
							stack.append(member)
					print(stack)

				else:

					for member in gp.adj_list[node]:
						if member != NodeList[node].message_list[0]: 
							if NodeList[member].message_list[3] == 0 and NodeList[member].message_list[4] != 1:
								NodeList[member].set_source_dest(node, gp.destination)
								NodeList[member].change_value(node, NodeList[node].message_list[3] + 1)
								NodeList[member].append_neighbours(node)
								stack.append(member)
							else:
								if NodeList[member].message_list[3] > (NodeList[node].message_list[3] + 1):
									NodeList[member].erase_list(member)
									NodeList[member].set_source_dest(node, gp.destination)
									NodeList[member].change_value(node, NodeList[node].message_list[3] + 1)
									NodeodeList[member].append_neighbours(node)


	for a in NodeList:				
		print(a.message_list)


	print(distances)



	# send message for identification of the devices that is in the communication range
	# def find connected devices 

	#deg = NodeList[source].get_connected(source, adj_list)


if __name__ == "__main__":
	main()
