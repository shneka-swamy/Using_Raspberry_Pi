# This program is used to discover the devices in the nearby area
# This program was taken from the example provided by digi xbee devices documentation


import time

from digi.xbee.models.status import *
from digi.xbee.devices import *

def main():
    device = XBeeDevice("/dev/ttyS0", 9600)
    rem = []

    try:
        device.open()

        xbee_net = device.get_network()
        # To check how the RSSI can be received
        #xbee_net.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF, DiscoveryOptions.APPEND_RSSI})
        #xbee_net.set_discovery_options({DiscoveryOptions.APPEND_RSSI})

        xbee_net.set_discovery_timeout(15)
        xbee_net.clear()
        

        def callback_device_discovered(remote):
            print("Device discovered is %s" %remote)
            rem.append(str(remote).split()[0])
            #send_message(remote)

        def callback_discovery_finished(status):
            if status == NetworkDiscoveryStatus.SUCCESS:
                print("Discovery process finished successfully")
            else:
                print("Discovery process not successful")

        xbee_net.add_device_discovered_callback(callback_device_discovered)
        xbee_net.add_discovery_process_finished_callback(callback_discovery_finished)
        xbee_net.start_discovery_process()

        print("Discovering Remote XBee Devices.")

        while xbee_net.is_discovery_running():
            time.sleep(0.1)

    finally:
        if device is not None and device.is_open():
            print(rem)

            # This is used to send message to the discovered device
            # Further iterations can be done to sequentially send the inforamtion to all devices in the range required.
            remote_device = RemoteXBeeDevice(device,XBee64BitAddress.
                                             from_hex_string(rem[0]))
            device.send_data(remote_device,"Hello XBee!!")
            device.close()

if __name__ == '__main__':
    main()
