from digi.xbee.devices import *

def main():
    device = XBeeDevice("/dev/ttyS0", 57600)

    try:
        device.open()

        print("Waiting for data")
        a = 0
        size = 0
        while a != 1:
            xbee_message = device.read_data()

            if xbee_message is not None:
                message = xbee_message.data.decode().split()
                print(message)
                size +=1
                a = len(message)
            
        

    finally:
        if device is not None and device.is_open():
            print(size)
            device.close()


if __name__ == '__main__':
    main()
