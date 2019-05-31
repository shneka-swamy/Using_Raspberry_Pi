from digi.xbee.devices import XBeeDevice
from digi.xbee.packets.base import DictKeys

def main():
    device = XBeeDevice("/dev/ttyS0", 9600)
    A_O = -50
    d_O = 1
    rssi_val = []

    # Formula used to calculate distance from RSSI
    # RSSI = -10*n log(d/d_O) + A_O
    # Where A_O is the RSSI for d_O = 1m
    # By performing the experiments the value of RSSI is found to be 50
    
    try:
        device.open()

        def packets_received_callback(packet):
            packet_dict = packet.to_dict()
            api_data = packet_dict[DictKeys.FRAME_SPEC_DATA][DictKeys.API_DATA]
            data = api_data[DictKeys.RF_DATA]
            rssi = api_data[DictKeys.RSSI]
            rssi_val.append(rssi)
            print(rssi)
            
        device.add_packet_received_callback(packets_received_callback)

        print("Waiting for data ...\n")
        input()


    # The value of the distance obtained is approximate to a few centimeters
    # And hence we can choose to use an average value instead of an actual value
    # This small variation in the distance should not affect the algorithm by a lot
    finally:
        if device is not None and device.is_open():
            print("\n")
            d_base = (A_O - ((-1)*rssi_val[0]))/20.0
            relative_distance = 10 ** d_base 
            print(relative_distance)
            device.close()


if __name__ == "__main__":
    main()
