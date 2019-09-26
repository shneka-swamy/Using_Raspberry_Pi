
import time

from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *


PORT = "/dev/ttyS0"
BAUD_RATE = 250000


def main():
    print(" +---------------------------------------------+")
    print(" | XBee Python Library Discover Devices Sample |")
    print(" +---------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        
        xbee_network = device.get_network()

        xbee_network.set_discovery_timeout(15)  # 15 seconds.

        xbee_network.clear()
        
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

        
        def data_receive_callback(xbee_message):
            not_used =  xbee_message.data.decode()
        
        
        
        
        xbee_network.add_device_discovered_callback(callback_device_discovered)

        xbee_network.add_discovery_process_finished_callback(callback_discovery_finished)

        xbee_network.start_discovery_process()

        print("Discovering remote XBee devices...")

        while xbee_network.is_discovery_running():
            time.sleep(0.1)

        device.add_data_received_callback(data_receive_callback)
        
        device.set_sync_ops_timeout(0.05)
        while(True):
            print("Enter a message: ")
            message = input()
            print("Repetitions: ")
            reps = int(input())
            start_time = time.time()
            i = 0
            failed_transmissions = 0
            while(i < reps):
                try:
                    
                    device.send_data(remote_devices[0], message)
                    i+=1
                except TimeoutException:
                    print("Dropped packet number %s" %i)
                    time.sleep(0.1)
                    failed_transmissions+=1
                    continue
                    
            print("Success")
            print("Elapsed time: %s" %(time.time() - start_time))
            print("Drop rate: %s" %(failed_transmissions / reps))

    except InvalidOperatingModeException:
        print("Invalid mode error: Restart module")
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
