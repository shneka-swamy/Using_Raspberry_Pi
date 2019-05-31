# First broadcast a Hello to all the devices in the network

from digi.xbee.devices import *

# This function is used to print the details required
def print_det(data):
    data_list = data.split()
    print("Found a device: %s at a distance of %s" %(data_list[0], data_list[1]))

def main():
    device = XBeeDevice("/dev/ttyS0",9600)
    device.open()

    # REquired ???
    # xbee_list = ["0013A2004102FC32", "0013A2004102FC76", "0013A20040B31805", "0013A20040B317F6"]

    #This broadcast of data is used as the node discovery step.
    device.send_data_broadcast(str(device.get_64bit_addr()))

    # Wait for the devices to respond with their MAC address and approximate
    # distance

    try:
        def data_callback(xbee_message):
            data = xbee_message.data.decode("utf8")
            print_det(data)

        device.add_data_received_callback(data_callback)
        print("Waiting for a reply to connect")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
