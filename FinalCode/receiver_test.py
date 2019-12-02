from digi.xbee.devices import *

def receive_data(device, new_list):
    
    device.open()

    try:
        list_val = []
        print("Waiting for data...\n")
        #count = 0
        flag = True

        while flag:
            xbee_message = device.read_data()

            if xbee_message is not None:
               string_val = xbee_message.data.decode().split()
               list_val += string_val 

               if count == 50:
                flag = False
                

    finally:
        if device is not None and device.is_open():
            print("Entered")
            device.close()

    return new_list

def main():
    new_list = []

    device = XBeeDevice("/dev/ttyUSB3", 115200)
    
    open_flag = True

    while open_flag:
        new_list = receive_data(device, new_list)
        #if new_list[-1] == 'f':
        #    open_flag = False

    print(len(new_list))


if __name__ == '__main__':
    main()