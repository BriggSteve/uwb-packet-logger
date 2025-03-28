from uwb_packet import UWBPacket
import time

def mock_receive_bytes():
    # Simulate receiving a packet every second
    pkt = UWBPacket(device_id=1, timestamp=int(time.time()*1000), x=1.0, y=2.0, z=3.0)
    return pkt.to_bytes()

def main():
    print("Starting UWB Packet Logger...")
    while True:
        raw = mock_receive_bytes()
        pkt = UWBPacket.from_bytes(raw)
        print(pkt)
        time.sleep(1)

if __name__ == "__main__":
    main()
