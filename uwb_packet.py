import struct

class UWBPacket:
    STRUCT_FORMAT = '<BBIfffBH'  # Added 1 byte for command
    START_BYTE = 0xAA

    def __init__(self, device_id, timestamp, x, y, z, command):
        self.device_id = device_id
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.z = z
        self.command = command

    def to_bytes(self):
        partial = struct.pack(
            '<BBIfffB',
            self.START_BYTE,
            self.device_id,
            self.timestamp,
            self.x, self.y, self.z,
            self.command
        )
        crc = self.calculate_crc(partial)
        return partial + struct.pack('<H', crc)

    @staticmethod
    def from_bytes(data: bytes):
        if len(data) != 21:
            raise ValueError("Invalid packet length")
        start, device_id, timestamp, x, y, z, command, crc = struct.unpack('<BBIfffBH', data)
        if start != UWBPacket.START_BYTE:
            raise ValueError("Invalid start byte")
        if UWBPacket.calculate_crc(data[:-2]) != crc:
            raise ValueError("CRC check failed")
        return UWBPacket(device_id, timestamp, x, y, z, command)

    @staticmethod
    def calculate_crc(data: bytes) -> int:
        return sum(data) & 0xFFFF

    def __repr__(self):
        return f"<UWBPacket ID={self.device_id} Cmd={self.command} Time={self.timestamp} X={self.x:.2f} Y={self.y:.2f} Z={self.z:.2f}>"
