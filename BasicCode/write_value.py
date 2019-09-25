#Sets up communication between the required devices.

from digi.xbee.devices import *

def main():
    device = XBeeDevice("/dev/ttyUSB0",115200)

    device.open()

    #To broadcast the message use

    # device.send_data_broadcast("Hello Xbee :)")

    # To send the message to a particular user
    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string
                                ("0013A2004102FC32"))
    
    # This part is included to change the power in the device, once the device power is set it does not change unless specified to
    # This changes the power of the device in which the program is run
    # The print statements are included to check for the actual power scale
   
    print(device.get_power_level())
    device.set_power_level(PowerLevel.LEVEL_LOWEST)
    print(device.get_power_level())
    
    # This command is used to send the information from one xbee to another.
    device.send_data(remote_device,"Hello XBee!!")

    try:
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

