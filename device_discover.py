# This program is used to discover the devices in the nearby area
# This program was taken from the example provided by digi xbee devices documentation


import time

from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice

def main():
    device = XBeeDevice("/dev/ttyS0", 9600)

    try:
        device.open()

        xbee_net = device.get_network()
        xbee_net.set_discovery_timeout(15)
        xbee_net.clear()

        def callback_device_discovered(remote):
            print("Device discovered is %s" %remote)

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
            device.close()

if __name__ == '__main__':
    main()
