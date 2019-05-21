# This program prints the data received from the other device upon receiving an user input
# This programis used to used to set the basic operation between two xbee s

from digi.xbee.devices import XBeeDevice

def main():
    device = XBeeDevice("/dev/ttyS0", 9600)

    try:
        device.open()

        def data_callback(xbee_message):
            address = xbee_message.remote_device.get_64bit_addr()
            data = xbee_message.data.decode("utf8")
            print("The data %s was received" %data)

        device.add_data_received_callback(data_callback)

        print("Waiting for the data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
