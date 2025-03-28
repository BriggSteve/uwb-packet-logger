import struct

class UWBPacket:
    STRUCT_FORMAT = '<BBIfffH'
    START_BYTE = 0xAA

    def __init__(self, device_id, timestamp, x, y, z):
        self.device_id = device_id
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.z = z

    def to_bytes(self):
        partial = struct.pack('<BBIfff', self.START_BYTE, self.device_id,
                              self.timestamp, self.x, self.y, self.z)
        crc = self.calculate_crc(partial)
        return partial + struct.pack('<H', crc)

    @staticmethod
    def from_bytes(data: bytes):
        if len(data) != 20:
            raise ValueError("Invalid packet length")
        start, device_id, timestamp, x, y, z, crc = struct.unpack('<BBIfffH', data)
        if start != UWBPacket.START_BYTE:
            raise ValueError("Invalid start byte")
        if UWBPacket.calculate_crc(data[:-2]) != crc:
            raise ValueError("CRC check failed")
        return UWBPacket(device_id, timestamp, x, y, z)

    @staticmethod
    def calculate_crc(data: bytes) -> int:
        return sum(data) & 0xFFFF

    def __repr__(self):
        return f"<UWBPacket ID={self.device_id} Time={self.timestamp} X={self.x:.2f} Y={self.y:.2f} Z={self.z:.2f}>"
