from digi.xbee.devices import *
from digi.xbee.util import *


def transmit():
    print ("Starting program")
    # Instantiate an XBee device object.
    local_xbee = XBeeDevice("/dev/ttyUSB2", 115200)
    # Open the device connection.
    try:
        local_xbee.open()
        
        def data_received_callback(xbee_message):
            address = xbee_message.remote_device.get_64bit_addr()
            data = xbee_message.data.decode("utf8")
            print("Received data from %s: %s" % (address, data))
        
        local_xbee.add_data_received_callback(data_received_callback)
        
        print("Waiting for the data...\n")
        input()
        
        

    finally:
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()

if __name__ == '__main__':
    main()
