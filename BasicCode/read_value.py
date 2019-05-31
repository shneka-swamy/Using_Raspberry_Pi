#This program is used to set communication between two different xbee
# Connected to a raspberry pi

#This program reads the data at first and then upon receiving an input sends
#the data to the device it received the data from

#This program uses the information provided in the digi website

from digi.xbee.devices import *

def main():
    device = XBeeDevice("/dev/ttyS0", 9600)

    try:
        device.open()

        def data_callback(xbee_message):
            # Can this address be used in place of the actual MAC Address provided.
            address = xbee_message.remote_device.get_64bit_addr()
            data = xbee_message.data.decode("utf8")
            print("The data %s was received" %data)

        device.add_data_received_callback(data_callback)

        print("Waiting for the data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A2004102FC76"))
            device.send_data(remote_device, "Hello Partner")
            device.close()


if __name__ == '__main__':
    main()

