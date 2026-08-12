import ConnectionStatus from "./ConnectionStatus";

export default function FleetHeader({ currentDevice, anomalyCount, connected }) {
  return (
    <header className="fleet-header">
      <div className="fleet-header-title">
        <h1>AGV Fleet Monitor</h1>
        <span className="fleet-header-device">{currentDevice || "—"}</span>
      </div>
      <div className="fleet-header-meta">
        <span className="anomaly-count">
          {anomalyCount} anomal{anomalyCount === 1 ? "y" : "ies"}
        </span>
        <ConnectionStatus connected={connected} />
      </div>
    </header>
  );
}
