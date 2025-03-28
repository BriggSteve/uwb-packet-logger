import time
from uwb_packet import UWBPacket

start = time.time()

def mock_receive_bytes():
    # Relative uptime in ms to avoid overflow
    timestamp = int((time.time() - start) * 1000)
    pkt = UWBPacket(device_id=1, timestamp=timestamp, x=1.0, y=2.0, z=3.0)
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
