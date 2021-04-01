import serial
import time
import keyboard
import random
import math
import trig
import signal
import sys
import struct

class Irobot():

	def __init__(self, port, baudrate):
		# Defaults set to COM6 and 57600 baud. 
		# The robot should always be run from 57600 baud unless not possible with the hardware.
		# COM6 would be a default on windows. Linux will require some '/dev/ttyUSB[port]'.
		self.ser = serial.Serial(port, baudrate)
		self.safe_start()
		self.running = False
		self.wall_colider = True
		self.timeToStop = 0

	def write_serial(self, array_to_write):
		if array_to_write == '\x89\x00\x00\x00\x00':
			self.running = False
		self.ser.write(array_to_write)

	def read_serial(self, array_to_read):
		return self.ser.read()

	def stop(self):
		self.write_serial(b'\x89\x00\x00\x00\x00')
		self.running = False

	def append_time(self, timeToAppend):
		self.running = True
		self.timeToStop = time.time() + timeToAppend

	def check_time_expired(self):
		if time.time() >= self.timeToStop:
			self.wall_colider = True
			return True
		return False

	def check_virtual_wall(self):
		array = bytearray()
		array.append(149) #Opcode to recieve packets from the iRobot
		array.append(1) #Recieve one packets
		array.append(13) #Virtual Wall
		self.write_serial(array)
		virtual_wall  = self.ser.read()
		print(virtual_wall)
		##time.sleep(0.1)
		return virtual_wall == b'\x01'

	def check_wall(self):
		array = bytearray()
		array.append(149) #Opcode to recieve packets from the iRobot
		array.append(1) #Recieve one packets
		array.append(7) # Wall
		self.write_serial(array)
		wall  = int.from_bytes(self.ser.read(),byteorder='big') & 3
		print(wall)
		##time.sleep(0.1)
		return wall > 0

	# Starts the robot up in safe mode to prevent overheating, crashes, etc. Gives the robot time to sleep before operation.
	# As you may notice, the way all of these methods work is through sending serial over UART to the robot.
	def safe_start(self):
		self.ser.write(b'\x80')
		self.ser.write(b'\x84')
		self.ser.write(b'')
		time.sleep(3)

	#Takes in a distance and a speed to move the robot. Distance can be positive or negative. Speed should be positive.
	def move(self, distance, speed):
		array = bytearray()
		# Start code for movement.
		start_code = 145

		# These lines of code determine how long the robot will run for based on its speed and distance.
		seconds = 0.0
		seconds = distance/speed
		seconds = abs(seconds)

		# A check for whether or not the speed is positive or negative.
		# Because of the way these robots function with serial commands, there has to be a 
		# two's complement transformation done to reverse the robot.
		if (distance > 0):
			speed = speed
			low_byte = 0
			high_byte = speed

		if (distance < 0):
			temp1 = 0xFF
			temp2 = speed
			temp3 = temp2 ^ temp1 
			temp3 = temp3 + 0x01
			low_byte = 255
			high_byte = int(temp3)
		
		# Appends all required data to the array to be sent to the robot.
		array.append(start_code)
		array.append(low_byte)
		array.append(high_byte)
		array.append(low_byte)
		array.append(high_byte)

		#print(array)
		self.ser.write(array)
		self.append_time(seconds)
		#print (seconds)

	def turn2(self, degrees):
		array = bytearray()
		array.append(137)
		newDeg = abs(int(200 / (90/degrees)))
		if newDeg < 255 and newDeg >= 0:
			array.append(0)
			array.append(newDeg)
		else:
			temp = newDeg % 255
			array.append(temp)
			array.append(255)
		if degrees < 0:
			print("Going left")
			array.append(0)
			array.append(1)
		else:
			print("Going right")
			array.append(255)
			array.append(255)

		self.ser.write(array)
		time.sleep(1.1)
		self.stop()

	#Use negative degrees to go left, positive degrees to go right.
	#True is left, false is right. Turns 90 degrees.
	def turn(self, degrees):
		array = bytearray()
		array.append(137)
		if (degrees < 0):
			newDeg = int((255+56) / (90/degrees))
			print(newDeg, degrees)
			lowByte = int(newDeg - 255)
			assert lowByte > 0 and lowByte <256 , "Error in low byte {}".format(lowByte)
			array.append(255)
			degrees = abs(degrees)
			array.append(lowByte)			
		else:
			newDeg = int(200 / (90/degrees))
			if newDeg < 255 and newDeg >= 0:
				array.append(0)
				array.append(newDeg)
			else:
				temp = newDeg % 255
				array.append(temp)
				array.append(255)

		# if (left_right):
		#	 array.append(0)
		#	 array.append(200)
		# else:
		#	 array.append(255)
		#	 array.append(55)
		array.append(0)
		array.append(0)

		self.ser.write(array)
		time.sleep(1.1)
		self.stop()

	def GetData(self):
		'''Returns data in binary for the distance the iRobot has gone and the angle at which it has turned in that order'''
		array = bytearray()
		array.append(149) #Opcode to recieve packets from the iRobot
		array.append(1) #Recieve two packets
		#array.append(19) #Distance
		#array.append(20) #Angle
		array.append(7) #Virtual Wall
		self.ser.write(array)
		print("Done with writing")

		newData  = int.from_bytes(self.ser.read(),byteorder='big') & 3
		print("Done with reading")

		time.sleep(1.1)
		self.ser.write(b'\x89\x00\x00\x00\x00')
		print(newData)
		return newData

	def GoRandom2(self):
		x = 0
		y = 0
		angle = 0
		distLimit = 2000
		self.move(200, 200)
		print("In random 2")
		while True:
			if self.running:
				print("Running is true", self.wall_colider, self.check_virtual_wall())
				if self.check_time_expired():
					print("Time expired :(")
					self.stop()
				if self.wall_colider and (self.check_virtual_wall() or self.check_wall()):
					self.stop()
					print("I detected a wall and I am stopping")
					self.wall_colider = False
					print("I am moving backward")
					self.move(-200, 200)
				continue

			if x >= distLimit:
				self.turn(angle)
				self.move(1500, 100)
				angle = 180
				x -= 5
			elif x <= -distLimit:
				self.turn(angle + 180)	
				self.move(1500, 100)
				angle = 0
				x += 5
			if y >= distLimit:
				self.turn(angle - 90)
				self.move(1500, 100)
				angle = 270
				y -= 5
			elif y <= -distLimit:
				self.turn(angle + 90)
				self.move(1500, 100)
				angle = 90
				y += 5
			else:
				randTurn = random.randint(10,100)
				self.turn(randTurn)
				angle += randTurn
				if angle < 0:
					while angle < 0:
						angle = angle + 360
				elif angle > 360:
					angle = angle % 360
				randDist = random.randint(0,200)
				randSpeed =  100 #random.randint(0,20)
				self.move(randDist, randSpeed)
				xypair = trig.PolarToCartesian(randDist, angle) # Get the x and y coordinates from the angle and the distance traveled.
				x += xypair[0]
				y += xypair[1]

	def GoRandom(self, xOrigin, yOrigin, angleOfRobot, distLimit):
		'''Takes the distance from the origin of the circle and the radius limit the iRobot is allowed to go as well as the robots angle with respect to the origin's coordinate system'''
		x = int(xOrigin)
		y = int(yOrigin)
		angle = int(angleOfRobot)
		distLimit = int(distLimit)

		while True:
			if x >= distLimit:
				self.turn(angle)
				self.move(1500, 100)
				angle = 180
				x -= 5
			elif x <= -distLimit:
				self.turn(angle + 180)
				self.move(1500, 100)
				angle = 0
				x += 5
			if y >= distLimit:
				self.turn(angle - 90)
				self.move(1500, 100)
				angle = 270
				y -= 5
			elif y <= -distLimit:
				self.turn(angle + 90)
				self.move(1500, 100)
				angle = 90
				y += 5
			else:
				randTurn = random.randint(0,120)
				self.turn(randTurn)
				angle += randTurn
				if angle < 0:
					while angle < 0:
						angle = angle + 360
				elif angle > 360:
					angle = angle % 360
				randDist = random.randint(0,200)
				randSpeed =  100 #random.randint(0,20)
				self.move(randDist, randSpeed)
				xypair = trig.PolarToCartesian(randDist, angle) # Get the x and y coordinates from the angle and the distance traveled.
				x += xypair[0]
				y += xypair[1]

def manual_control():

	robot = Irobot('/dev/ttyUSB0', 57600)
	check = 7
	while (check != 6):
		print("Enter a command: (1=forward, 2=backward, 3=turn left, 4=turn_right, 5=Get Data, 6=Random Movement with Center Default, 7=Random Movement w/ custom args, 8=exit to key commands")
		check = int(input())
		if (check == 1):
			robot.move(200,200)
		elif (check == 2):
			robot.move(-200,200)
		elif (check == 3):
			robot.turn2(-100)
		elif (check == 4):
			robot.turn2(100)
		elif (check == 5):
			test = robot.GetData()
			#print(test)
		elif (check == 6):
			robot.GoRandom2()
		elif (check == 7):
			xOrg = 0 #input("What is the initial x coordinate?: ")
			yOrg = 0 #input("What is the initial y coordinate?: ")
			angle = 0 #input("What angle is the robot at? (right being 0 degrees): ")
			dist = 2000 #input("What is the robots radius limit? (in mm): ")
			robot.GoRandom(xOrg, yOrg, angle, dist)
		else:
			break

	print ("Use Key Controls (WASD) to move and E to exit.")
	while (True):
		if (keyboard.is_pressed('w')):
			robot.move(200,200)
		elif (keyboard.is_pressed('s')):
			robot.move(-200,200)
		elif (keyboard.is_pressed('a')):
			robot.turn(-15)
		elif (keyboard.is_pressed('d')):
			robot.turn(15)
		elif (keyboard.is_pressed('e')):
			break

	robot.ser.close()

if __name__ == '__main__':
	manual_control()