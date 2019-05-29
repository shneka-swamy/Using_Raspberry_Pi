from digi.xbee.devices import *
from digi.xbee.packets.base import DictKeys

# All the functions need to be sent the device object and must be opened and closed in the function
def send_msg(address, distance, device):
    device.open()

    remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(address))
    device.send_data(remote_device, str(device.get_64bit_addr())+ " " + str(distance))

    device.close()

#This function is used to print data in required format.
def print_details(address, distance):
    print("Received Request From: %s at a distance of: %s" %(address, distance))

def get_RSSI(device):
    # Defining the constants
    A_O = -50
    d_O = 1
    rssi_val = []
    revd_data = []
    
    # Formula used to calculate distance from RSSI
    # RSSI = -10*n log(d/d_O) + A_O
    # Where A_O is the RSSI for d_O = 1m
    # By performing the experiments the value of RSSI is found to be 50
    
    try:
        device.open()

        def packets_received_callback(packet):
            packet_dict = packet.to_dict()
            api_data = packet_dict[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
            revd_data.append(api_data[DictKeys.RF_DATA])
            rssi_val.append(api_data[DictKeys.RSSI])
            
        device.add_packet_received_callback(packets_received_callback)

        print("Waiting for call ...\n")
        input()


    # The value of the distance obtained is approximate to a few centimeters
    # And hence we can choose to use an average value instead of an actual value
    # This small variation in the distance should not affect the algorithm by a lot
    finally:
        if device is not None and device.is_open():
            device.close()
            
    print(rssi_val)
    d_base = (A_O - ((-1)*rssi_val[0]))/20.0
    relative_distance = 10 ** d_base
    address_reqd = revd_data[0].decode()

    print_details(address_reqd, relative_distance)

    return [address_reqd, relative_distance]
    
def main():
    device = XBeeDevice("/dev/ttyS0", 9600)
    
    [address_reqd, relative_distance] = get_RSSI(device)
    send_msg(address_reqd, relative_distance, device)

if __name__ == "__main__":
    main()
    
