# AGV Fleet Monitor

Real-time telemetry dashboard for a fleet of AGVs (Automated Guided Vehicles), with
unsupervised ML-based anomaly detection for predictive maintenance.

## What it does

- Simulates live sensor telemetry (motor current, joint torque, temperature, vibration)
  from a fleet of AGV arms
- Ingests and persists readings via a FastAPI backend
- Flags anomalous readings in real time using an Isolation Forest model, trained on
  historical telemetry — no labeled failure data required
- Visualizes live per-device metrics on a React dashboard, with anomalies highlighted
  directly on the charts and surfaced in a live alert feed

## Why

Fixed-threshold alerting misses gradual degradation (e.g. slowly rising vibration
before a bearing fails). An unsupervised anomaly model catches multi-signal drift
that simple rules can't, without needing pre-labeled failure examples — which are
rarely available for physical equipment early in its life.

## Architecture

Simulator (Python) --> FastAPI /ingest --> SQLite --> FastAPI /readings
| |
Isolation Forest React dashboard
(scores each reading) (polls + charts)


## Tech stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **ML:** scikit-learn (Isolation Forest), pandas
- **Frontend:** React (Vite), Recharts
- **Data:** simulated AGV sensor stream (swappable for real telemetry)

## Project structure

```text
agv-fleet-monitor/
├── backend/
│   ├── simulator/
│   │   └── generate.py          # Fake sensor stream generator
│   ├── models/
│   │   └── db.py                # SQLAlchemy models + DB session
│   ├── api/
│   │   └── main.py              # FastAPI app (ingest, devices, readings)
│   ├── ai/
│   │   └── train.py             # Isolation Forest training script
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── api/
        │   └── fleetApi.js      # Data fetching
        ├── hooks/               # useDevices, useReadings (polling)
        └── components/          # DeviceTabs, StatusBar, AnomalyFeed
```


## Running it locally

Requires Python 3.11+ and Node 18+.

```bash
# 1. Backend setup
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Start the API
cd api && uvicorn main:app --reload --port 8000

# 3. In a new terminal — start the simulator
cd backend/simulator && python generate.py

# 4. Let it run ~2 minutes, then train the anomaly model
cd backend/ai && python train.py
# restart the API afterward so it picks up the trained model

# 5. In a new terminal — start the frontend
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

## What this project demonstrates

- Real-time data pipeline design (ingestion → storage → API → live UI)
- Unsupervised ML applied to a genuine engineering problem (predictive maintenance),
  not bolted on for its own sake
- React component architecture: data-fetching hooks separated from presentational
  components
- End-to-end ownership: simulator, backend, ML layer, and frontend all built and
  wired together

## Possible extensions

- Swap SQLite for TimescaleDB for real time-series scale
- LLM-generated plain-English maintenance notes from anomaly context
- Docker Compose for one-command startup
- Real AGV hardware integration in place of the simulator
