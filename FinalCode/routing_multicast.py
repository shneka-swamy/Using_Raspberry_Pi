# Multicast Routing

import graph as gp

class Nodes:
	"""docstring for ClassName"""

	def __init__(self, arg, shift):
		# The message list considers the required message
		# [source, Effective Degree, Hop, destination, Mode of the Node]  
		# The modes of the nodes are defined as 0: Relay, 1: Source and 2: Destination
		# The message list also contains the nearby neighbours
		# The elements in the adj list (are appended when the member is visited)
		self.message_list = [arg]*(3 + shift)
		self.message_list.append('R')
	
	def set_source_dest(self, source, dest, no_dest):
		self.message_list[0] = source

		for i in range(0, no_dest):
			self.message_list[3+i] = dest[i]

	def change_value(self, source, hop):
		self.message_list[1] = len(gp.adj_list[source])
		self.message_list[2] = hop

	def append_neighbours(self, neighbour):
		self.message_list += neighbour

	def erase_list(self, source, shift):
		self.message_list = self.message_list[0:(3+shift)]
	
	def destination_found(self, dest, shift):
		for j in range(3, 3+ shift):
			if self.message_list[j] == dest:
				self.message_list[j] = -1

	def destination_available(self, shift):
		for i in range(3, 3+shift):
			if self.message_list[i] != -1:
				return True
		return False


# Path is the list that contains all the paths
# node is the element adjacent to the list
def get_path(path, node, NodeList, dest):
	create_path = [(dest, 0)]
	
	while dest != gp.source:
		create_path.append((NodeList[dest].message_list[0], NodeList[dest].message_list[1]))
		dest = NodeList[dest].message_list[0]

	path.append(create_path)

	print(create_path)	


def main():

	no_dest = len(gp.destination)

	NodeList = []
	for i in range(0,10):
		NodeList.append(Nodes(0, no_dest))

	NodeList[gp.source].message_list[3 + no_dest] = 'S'

	#source_include = 3
	#NodeList[source_include].message_list[3 + no_dest] = 'S'

	source_include = 5
	NodeList[source_include].message_list[3 + no_dest] = 'S'


	neigh_list = []
	distances = []
	path = []
	flag = 1
	stack = [gp.source] 
	
	while len(stack) != 0:

		copy_stack = stack.copy()
		del stack[:]	
		print(copy_stack)

		for node in copy_stack:
			
			# Create the neighbour list removing all sources and the source of the current node
			for mem in gp.adj_list[node]:
				
				if NodeList[mem].message_list[3 + no_dest] == 'S' or NodeList[node].message_list[0] == mem:
					pass
				
				# This function checks if the path or the final destination can be reached with minimum number of hops
				elif NodeList[mem].message_list[2]  == 0 or (NodeList[mem].message_list[2] > (NodeList[node].message_list[2] + 1)):
					if mem in gp.destination:
						
						if NodeList[node].message_list[3] == 0:
							dest = gp.destination
						else:
							dest = 	NodeList[node].message_list[3 : 3+ no_dest]

						NodeList[mem].set_source_dest(node,dest , no_dest)	
						NodeList[mem].destination_found(mem, no_dest)
						NodeList[mem].change_value(node, NodeList[node].message_list[2] + 1)
						NodeList[mem].append_neighbours(gp.adj_list[node])
						

						get_path(path, node, NodeList, mem)
						distances.append(NodeList[mem].message_list[2] + 1)
		
						if NodeList[mem].destination_available(no_dest):
							stack.append(mem)

					else:
						if NodeList[node].message_list[3] == 0:
							dest = gp.destination
						else:
							dest = 	NodeList[node].message_list[3 : 3+ no_dest]

						NodeList[mem].set_source_dest(node, dest, no_dest)
						NodeList[mem].change_value(node, NodeList[node].message_list[2] + 1)
						NodeList[mem].append_neighbours(gp.adj_list[node])

						if NodeList[mem].destination_available(no_dest):
							stack.append(mem)
				
				else:
					pass

				#print(NodeList[mem].message_list)
				# If all the destinations are already found, don't look at my neighbour list
			del neigh_list[:]

	for a in NodeList:				
		print(a.message_list)

	print(path)
	print(distances)

if __name__ == "__main__":
	main()