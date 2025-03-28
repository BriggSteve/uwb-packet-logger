import time
import psycopg2
import os
from uwb_packet import UWBPacket
import random
# Pull connection info from environment
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432)
)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS packets (
        id SERIAL PRIMARY KEY,
        device_id INTEGER,
        timestamp BIGINT,
        x REAL,
        y REAL,
        z REAL
    )
""")
conn.commit()

start = time.time()


def mock_receive_bytes(device_id):
    timestamp = int((time.time() - start) * 1000)

    x = round(random.uniform(1.0, 5.0), 2)
    y = round(random.uniform(1.0, 5.0), 2)
    z = round(random.uniform(1.0, 5.0), 2)

    # Randomly assign commands (10% chance of HELLO_WORLD)
    command = 0x01 if random.random() < 0.1 else 0x00

    pkt = UWBPacket(device_id, timestamp, x, y, z, command)
    return pkt.to_bytes()


def main():
    print("Logging packets to Postgres...")
    while True:
        for device_id in range(1, 4):  # Simulate 3 devices
            raw = mock_receive_bytes(device_id)
            pkt = UWBPacket.from_bytes(raw)

            cur.execute(
                "INSERT INTO packets (device_id, timestamp, x, y, z) VALUES (%s, %s, %s, %s, %s)",
                (pkt.device_id, pkt.timestamp, pkt.x, pkt.y, pkt.z)
            )
            conn.commit()

            print(f"Stored: {pkt}")

        time.sleep(10)  # Generate one round of packets every 10s


if __name__ == "__main__":
    main()
