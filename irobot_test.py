import serial
import time
import keyboard
import random
import math
import trig

class Irobot():
    pass

    def __init__(self, port, baudrate):
        # Defaults set to COM6 and 57600 baud. 
        # The robot should always be run from 57600 baud unless not possible with the hardware.
        # COM6 would be a default on windows. Linux will require some '/dev/ttyUSB[port]'.
        self.ser = serial.Serial(port='COM3', baudrate=57600)
        self.safe_start()
        

    # Starts the robot up in safe mode to prevent overheating, crashes, etc. Gives the robot time to sleep before operation.
    # As you may notice, the way all of these methods work is through sending serial over UART to the robot.
    def safe_start(self):
        self.ser.write(b'\x80')
        self.ser.write(b'\x84')
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

        # print(array)
        self.ser.write(array)
        # print (seconds)
        time.sleep(seconds)
        self.ser.write(b'\x89\x00\x00\x00\x00')

    #Use negative degrees to go left, positive degrees to go right.
    #True is left, false is right. Turns 90 degrees.
    def turn(self, degrees):
        array = bytearray()
        array.append(137)
        if (degrees < 0):
            newDeg = int((255+56) / (90/degrees))
            lowByte = int(newDeg - 255)
            array.append(255)
            degrees = abs(degrees)
            array.append(lowByte)            
        else:
            array.append(0)
            newDeg = int(200 / (90/degrees))
            array.append(newDeg)

        # if (left_right):
        #     array.append(0)
        #     array.append(200)
        # else:
        #     array.append(255)
        #     array.append(55)
        array.append(0)
        array.append(0)

        self.ser.write(array)
        time.sleep(1.1)
        self.ser.write(b'\x89\x00\x00\x00\x00')

    def GetData(self):
        '''Returns data in binary for the distance the iRobot has gone and the angle at which it has turned in that order'''
        array = bytearray()
        array.append(149) #Opcode to recieve packets from the iRobot
        array.append(2) #Recieve two packets
        array.append(19) #Distance
        array.append(20) #Angle
        self.ser.write(array)

        newData = self.ser.read(9)

        time.sleep(1.1)
        self.ser.write(b'\x89\x00\x00\x00\x00')
        return newData

    def GoRandom(self, distFromOrigin, angleFromOrigin, distLimit):
        '''Takes the distance from the origin of the circle and the radius limit the iRobot is allowed to go'''
        xypair = trig.PolarToCartesian(distFromOrigin, angleFromOrigin)
        x = xypair[0]
        y = xypair[1]
        while True:
            rawData = self.GetData()
            distance = (rawData << 24) & 0xFFFF00
            angle = rawData << 56
            xypair = trig.PolarToCartesian(distFromOrigin + distance, angleFromOrigin + angle)
            x = xypair[0]
            y = xypair[1]
            if x >= 10000:
                if angle > 180:
                    self.turn(-(angle % 180))
                    self.move(-500, 20)
                elif angle < 180:
                    self.turn(angle % 180)
                    self.move(-500, 20)
                else:
                    self.move(-500, 20)
            elif x <= 10000:
                if angle > 0:
                    self.turn(-angle)
                    self.move(-500, 20)
                else:
                    self.move(-500, 20)
            if y >= 10000:
                if angle > 90:
                    self.turn(-(angle % 90))
                    self.move(-500, 20)
                elif angle < 90:
                    self.turn(angle % 90)
                    self.move(-500, 20)
                else:
                    self.move(-500, 20)
            elif y <= 10000:
                if angle > 270:
                    self.turn(-(angle % 270))
                    self.move(-500, 20)
                elif angle < 270:
                    self.turn(angle % 270)
                    self.move(-500, 20)
                else:
                    self.move(-500, 20)
            else:
                self.trun(random.randint(0,359))
                self.move(random.randint(0,200),random.randint(0,200))




def manual_control():
    robot = Irobot('COM3', 57600)
    check = 0
    while (check != 6):
        print("Enter a command: (1=forward, 2=backward, 3=turn left, 4=turn_right, 5=Get Data, 6=exit to key commands")
        check = int(input())
        if (check == 1):
            robot.move(200,200)
        elif (check == 2):
            robot.move(-200,200)
        elif (check == 3):
            robot.turn(-15)
        elif (check == 4):
            robot.turn(15)
        elif (check == 5):
            test = robot.GetData()
            print(test)
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