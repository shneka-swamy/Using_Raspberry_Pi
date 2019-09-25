from digi.xbee.devices import *
from digi.xbee.util import *



def main():
    print ("Starting program")
    # Instantiate an XBee device object.
    local_xbee = XBeeDevice("/dev/ttyUSB0", 115200)
    # Open the device connection.
    try:
        local_xbee.open()

        remote_device = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string
                                                ("0013A2004102FC76"))


        local_xbee.send_data(remote_device, "HELLO!") 

    finally:
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()

if __name__ == '__main__':
    main()
