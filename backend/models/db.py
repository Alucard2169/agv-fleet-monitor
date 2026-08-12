from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fleet.db")
DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    air_temperature_c = Column(Float)
    process_temperature_c = Column(Float)
    rotational_speed_rpm = Column(Float)
    torque_nm = Column(Float)
    tool_wear_min = Column(Float)
    machine_failure = Column(Boolean, default=False)  # real ground-truth label from the dataset
    failure_type = Column(String, default="None")     # TWF / HDF / PWF / OSF / RNF / None
    is_anomaly = Column(Integer, default=0)            # model's prediction, scored at ingest

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
