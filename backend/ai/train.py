import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from models.db import SessionLocal, SensorReading

FEATURES = [
    "air_temperature_c", "process_temperature_c",
    "rotational_speed_rpm", "torque_nm", "tool_wear_min",
]

def load_data():
    db = SessionLocal()
    rows = db.query(SensorReading).all()
    db.close()
    data = [
        {**{f: getattr(r, f) for f in FEATURES}, "machine_failure": r.machine_failure}
        for r in rows
    ]
    return pd.DataFrame(data)

def train():
    df = load_data()
    print(f"Loaded {len(df)} rows")

    if len(df) < 50:
        print("Not enough data yet — let the replayer run longer.")
        return

    model = IsolationForest(
        n_estimators=200,
        contamination=0.034,
        random_state=42,
    )
    model.fit(df[FEATURES])

    joblib.dump(model, os.path.join(os.path.dirname(__file__), "model.joblib"))
    print("Model trained and saved to backend/ai/model.joblib")

    preds = model.predict(df[FEATURES])
    predicted_anomaly = (preds == -1).astype(int)
    actual_failure = df["machine_failure"].astype(int)

    print(f"\nFlagged {predicted_anomaly.sum()} / {len(df)} rows as anomalies "
          f"({predicted_anomaly.mean():.1%})")

    print("\nEvaluated against real ground-truth failure labels:")
    print(classification_report(actual_failure, predicted_anomaly, target_names=["Normal", "Failure"], zero_division=0))
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(actual_failure, predicted_anomaly))

if __name__ == "__main__":
    train()
