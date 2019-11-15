import serial
import time
import keyboard

#Starts the robot up in safe mode to prevent overheating, crashes, etc. Gives the robot time to sleep before operation.
def safe_start():
    ser.write(b'\x80')
    ser.write(b'\x84')
    time.sleep(3)

#Takes in a distance and a speed to move the robot. Distance can be positive or negative. Speed should be positive.
def move(distance, speed):
    array = bytearray()
    start_code = 145

    seconds = 0.0
    seconds = distance/speed
    seconds = abs(seconds)

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
        print(hex(low_byte))
        print(hex(high_byte))
    
    array.append(start_code)
    array.append(low_byte)
    array.append(high_byte)
    array.append(low_byte)
    array.append(high_byte)
    print(array)
    ser.write(array)
    print (seconds)
    time.sleep(seconds)
    ser.write(b'\x89\x00\x00\x00\x00')

#True is left, false is right. Turns 90 degrees.
def turn(left_right):
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

    ser.write(array)
    time.sleep(1.1)
    ser.write(b'\x89\x00\x00\x00\x00')

ser = serial.Serial(port='COM6', baudrate=57600)
print("Serial Port Name:", ser.name)
print("Baudrate:", ser.baudrate)
safe_start()

check = 0
while (check != 5):
    print("Enter a command: (1=forward, 2=backward, 3=turn left, 4=turn_right, 5=exit to key commands")
    check = int(input())
    if (check == 1):
        move(200,200)
    elif (check == 2):
        move(-200,200)
    elif (check == 3):
        turn(True)
    elif (check == 4):
        turn(False)
    else:
        break

print ("Use Key Controls (WASD) to move and E to exit.")
while (True):
    if (keyboard.is_pressed('w')):
        move(200,200)
    elif (keyboard.is_pressed('s')):
        move(-200,200)
    elif (keyboard.is_pressed('a')):
        turn(True)
    elif (keyboard.is_pressed('d')):
        turn(False)
    elif (keyboard.is_pressed('e')):
        break


ser.close()