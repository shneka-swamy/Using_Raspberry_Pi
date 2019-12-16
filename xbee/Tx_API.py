from digi.xbee.devices import *
from digi.xbee.util import *



def main():
    print ("Starting program")
    # Instantiate an XBee device object.
    local_xbee = XBeeDevice("/dev/ttyUSB1", 250000)
    # Open the device connection.
    
    local_xbee.open()

    remote_devices = []
    # Callback for discovered devices.
    def callback_device_discovered(remote):
        # remote_address = str(remote).split()[0]
        print("Device discovered: %s, inserting into list at element: %s" % (remote.get_64bit_addr(), len(remote_devices)))
        remote_devices.append(remote)

    # Callback for discovery finished.
    def callback_discovery_finished(status):
        if status == NetworkDiscoveryStatus.SUCCESS:
            print("Discovery process finished successfully.")
        else:
            print("There was an error discovering devices: %s" % status.description)
    
    remote_device = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string
    #                                ("0013A200419B580F"))
                                     ("0013A200419B5871"))
    
    message = "Test data for shneka! This message is about 100 bytes. This is going to get longer too! Yayatatatata"
    #message = "Shneka"
    try:
        for i in range(500):
            local_xbee.send_data(remote_device, message) 

    finally:
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()

if __name__ == '__main__':
    main()
