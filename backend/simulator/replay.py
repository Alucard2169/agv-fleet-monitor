import os
import time
from datetime import datetime, timezone
import pandas as pd
import requests

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "ai4i2020_prepared.csv"
)
API_URL = "http://localhost:8000/ingest"

def load_data():
    df = pd.read_csv(CSV_PATH, keep_default_na=False, na_values=[])
    before = len(df)
    df = df.dropna()
    dropped = before - len(df)
    if dropped:
        print(f"Dropped {dropped} rows with missing values")
    # Shuffle once so devices interleave in the stream instead of playing
    # as three long sequential blocks (the raw CSV is grouped by type).
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


def to_payload(row):
    return {
        "device_id": row["device_id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "air_temperature_c": round(float(row["air_temperature_c"]), 2),
        "process_temperature_c": round(float(row["process_temperature_c"]), 2),
        "rotational_speed_rpm": float(row["rotational_speed_rpm"]),
        "torque_nm": float(row["torque_nm"]),
        "tool_wear_min": float(row["tool_wear_min"]),
        "machine_failure": bool(row["machine_failure"]),
        "failure_type": row["failure_type"],
    }

def replay(interval_sec: float = 1.0):
    df = load_data()
    print(f"Replaying {len(df)} real machine readings (looping continuously)")
    while True:
        for _, row in df.iterrows():
            payload = to_payload(row)
            try:
                resp = requests.post(API_URL, json=payload)
                print(payload["device_id"], payload["failure_type"], "->", resp.status_code)

            except requests.exceptions.ConnectionError:
                print("API not reachable, is uvicorn running?")
            time.sleep(interval_sec)

if __name__ == "__main__":
    replay()
