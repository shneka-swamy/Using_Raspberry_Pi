import serial
import time
import keyboard

class Irobot():
    pass

    def __init__(self, port, baudrate):
        # Defaults set to COM6 and 57600 baud. 
        # The robot should always be run from 57600 baud unless not possible with the hardware.
        # COM6 would be a default on windows. Linux will require some '/dev/ttyUSB[port]'.
        self.ser = serial.Serial(port='COM6', baudrate=57600)
        

    # Starts the robot up in safe mode to prevent overheating, crashes, etc. Gives the robot time to sleep before operation.
    # As you may notice, the way all of these methods work is through sending serial over UART to the robot.
    def safe_start(self):
        ser.write(b'\x80')
        ser.write(b'\x84')
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

    #True is left, false is right. Turns 90 degrees.
    def turn(self, left_right):
        array = bytearray()
        array.append(137)
        if (left_right):
            array.append(0)
            array.append(200)
        else:
            array.append(255)
            array.append(55)
        array.append(0)
        array.append(0)

        self.ser.write(array)
        time.sleep(1.1)
        self.ser.write(b'\x89\x00\x00\x00\x00')

def manual_control():

    check = 0
    while (check != 5):
        print("Enter a command: (1=forward, 2=backward, 3=turn left, 4=turn_right, 5=exit to key commands")
        check = int(input())
        if (check == 1):
            move(200,200, ser)
        elif (check == 2):
            move(-200,200, ser)
        elif (check == 3):
            turn(True, ser)
        elif (check == 4):
            turn(False, ser)
        else:
            break

    print ("Use Key Controls (WASD) to move and E to exit.")
    while (True):
        if (keyboard.is_pressed('w')):
            move(200,200, ser)
        elif (keyboard.is_pressed('s')):
            move(-200,200, ser)
        elif (keyboard.is_pressed('a')):
            turn(True, ser)
        elif (keyboard.is_pressed('d')):
            turn(False, ser)
        elif (keyboard.is_pressed('e')):
            break

    ser.close()