from ucimlrepo import fetch_ucirepo
import pandas as pd
import os

dataset = fetch_ucirepo(id=601)
X = dataset.data.features.copy()
y = dataset.data.targets.copy()

df = pd.concat([X, y], axis=1)

# Kelvin -> Celsius for readability
df["air_temperature_c"] = df["Air temperature"] - 273.15
df["process_temperature_c"] = df["Process temperature"] - 273.15

# Map the 3 product quality variants to 3 fleet devices
type_map = {"L": "machine_L", "M": "machine_M", "H": "machine_H"}
df["device_id"] = df["Type"].map(type_map)

# Collapse the 5 failure-mode flags into one label
failure_cols = ["TWF", "HDF", "PWF", "OSF", "RNF"]
def failure_type(row):
    if row["Machine failure"] == 0:
        return "None"
    for col in failure_cols:
        if row[col] == 1:
            return col
    return "Unknown"

df["failure_type"] = df.apply(failure_type, axis=1)

out = df[[
    "device_id", "Rotational speed", "Torque", "Tool wear",
    "air_temperature_c", "process_temperature_c",
    "Machine failure", "failure_type",
]].rename(columns={
    "Rotational speed": "rotational_speed_rpm",
    "Torque": "torque_nm",
    "Tool wear": "tool_wear_min",
    "Machine failure": "machine_failure",
})

os.makedirs("data", exist_ok=True)
out.to_csv("data/ai4i2020_prepared.csv", index=False)
print(f"Saved {len(out)} rows to data/ai4i2020_prepared.csv")
print(out.head())
print("\nRows per device:\n", out["device_id"].value_counts())
