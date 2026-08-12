from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
import pandas as pd
import sys, os
import joblib
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.db import SessionLocal, SensorReading, init_db, get_db

app = FastAPI(title="AGV Fleet Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai", "model.joblib")
anomaly_model = None
FEATURES = ["air_temperature_c", "process_temperature_c", "rotational_speed_rpm", "torque_nm", "tool_wear_min"]

@app.on_event("startup")
def startup():
    init_db()
    global anomaly_model
    if os.path.exists(MODEL_PATH):
        anomaly_model = joblib.load(MODEL_PATH)
        print("Anomaly model loaded")
    else:
        print("No trained model found — run backend/ai/train.py first")

class ReadingIn(BaseModel):
    device_id: str
    timestamp: str
    air_temperature_c: float
    process_temperature_c: float
    rotational_speed_rpm: float
    torque_nm: float
    tool_wear_min: float
    machine_failure: bool
    failure_type: str

@app.post("/ingest")
def ingest_reading(reading: ReadingIn, db: Session = Depends(get_db)):
    if anomaly_model is not None:
        features = pd.DataFrame([[
            reading.air_temperature_c, reading.process_temperature_c,
            reading.rotational_speed_rpm, reading.torque_nm, reading.tool_wear_min,
        ]], columns=FEATURES)
        pred = anomaly_model.predict(features)[0]
        is_anomaly = 1 if pred == -1 else 0
    else:
        is_anomaly = 1 if reading.machine_failure else 0  # fallback until a model is trained

    row = SensorReading(
        device_id=reading.device_id,
        timestamp=datetime.fromisoformat(reading.timestamp),
        air_temperature_c=reading.air_temperature_c,
        process_temperature_c=reading.process_temperature_c,
        rotational_speed_rpm=reading.rotational_speed_rpm,
        torque_nm=reading.torque_nm,
        tool_wear_min=reading.tool_wear_min,
        machine_failure=reading.machine_failure,
        failure_type=reading.failure_type,
        is_anomaly=is_anomaly,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"status": "ok", "id": row.id, "is_anomaly": bool(is_anomaly)}

@app.get("/devices")
def list_devices(db: Session = Depends(get_db)):
    devices = db.query(SensorReading.device_id).distinct().all()
    return [d[0] for d in devices]

@app.get("/readings/{device_id}")
def get_readings(device_id: str, limit: int = 100, db: Session = Depends(get_db)):
    rows = (
        db.query(SensorReading)
        .filter(SensorReading.device_id == device_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "timestamp": r.timestamp.isoformat(),
            "air_temperature_c": r.air_temperature_c,
            "process_temperature_c": r.process_temperature_c,
            "rotational_speed_rpm": r.rotational_speed_rpm,
            "torque_nm": r.torque_nm,
            "tool_wear_min": r.tool_wear_min,
            "machine_failure": r.machine_failure,
            "failure_type": r.failure_type,
            "is_anomaly": r.is_anomaly,
        }
        for r in reversed(rows)
    ]
