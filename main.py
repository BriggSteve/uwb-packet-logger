import time
import psycopg2
import os
from uwb_packet import UWBPacket

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

def mock_receive_bytes():
    timestamp = int((time.time() - start) * 1000)
    pkt = UWBPacket(device_id=1, timestamp=timestamp, x=1.0, y=2.0, z=3.0)
    return pkt.to_bytes()

def main():
    print("Logging packets to Postgres...")
    while True:
        raw = mock_receive_bytes()
        pkt = UWBPacket.from_bytes(raw)

        cur.execute(
            "INSERT INTO packets (device_id, timestamp, x, y, z) VALUES (%s, %s, %s, %s, %s)",
            (pkt.device_id, pkt.timestamp, pkt.x, pkt.y, pkt.z)
        )
        conn.commit()

        print(f"Stored: {pkt}")
        time.sleep(10)

if __name__ == "__main__":
    main()
