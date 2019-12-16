from digi.xbee.devices import *
from digi.xbee.util import *
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *
from digi.xbee.exception import *
import time

messageCounter = 0
start_time = 0
end_time = 0

def main():
    print ("Starting program")
    # Instantiate an XBee device object.
    local_xbee = XBeeDevice("/dev/ttyUSB0", 250000)
    # Open the device connection.

    

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


    try:
        local_xbee.open()
    
        
        def data_received_callback(xbee_message):
            global messageCounter
            messageCounter += 1
            if messageCounter == 1:
                global start_time
                start_time = time.time()
            if messageCounter == 500:
                global end_time
                end_time = time.time()
                rate = (500*100)/(end_time - start_time)
                print(rate)
            
            if messageCounter % 10 == 0:
                print(messageCounter)
        
        local_xbee.add_data_received_callback(data_received_callback)
        
        print("Waiting for the data...\n")
        input()
        
        

    finally:
        global start_time, end_time
        print(end_time - start_time)
        print((500*100)/(end_time - start_time))
        if local_xbee is not None and local_xbee.is_open():
            local_xbee.close()

if __name__ == '__main__':
    main()
