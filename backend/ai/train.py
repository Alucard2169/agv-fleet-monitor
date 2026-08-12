import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from models.db import SessionLocal, SensorReading

FEATURES = ["motor_current_a", "joint_torque_nm", "temperature_c", "vibration_g"]

def load_data():
    db = SessionLocal()
    rows = db.query(SensorReading).all()
    db.close()
    data = [{f: getattr(r, f) for f in FEATURES} for r in rows]
    return pd.DataFrame(data)

def train():
    df = load_data()
    print(f"Loaded {len(df)} rows")

    if len(df) < 50:
        print("Not enough data yet — let the simulator run longer.")
        return

    model = IsolationForest(
        n_estimators=200,
        contamination=0.03,  # matches the ~3% anomaly rate in the simulator
        random_state=42,
    )
    model.fit(df[FEATURES])

    joblib.dump(model, os.path.join(os.path.dirname(__file__), "model.joblib"))
    print("Model trained and saved to backend/ai/model.joblib")

    # quick sanity check
    preds = model.predict(df[FEATURES])
    n_anomalies = (preds == -1).sum()
    print(f"Flagged {n_anomalies} / {len(df)} rows as anomalies ({n_anomalies/len(df):.1%})")

if __name__ == "__main__":
    train()
