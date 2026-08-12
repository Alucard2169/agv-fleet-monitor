import EmptyState from "./EmptyState";

export default function AnomalyFeed({ anomalies }) {
  return (
    <div className="anomaly-log">
      <div className="anomaly-log-header">Anomaly Log</div>
      <div className="anomaly-log-body">
        {anomalies.length === 0 ? (
          <EmptyState title="No anomalies detected" detail="Readings are within normal range." />
        ) : (
          anomalies.slice().reverse().map((r, i) => (
            <div className="anomaly-log-row" key={`${r.timestamp}-${i}`}>
              <span className="anomaly-log-time">{r.time}</span>
              <span className="anomaly-log-tag">{r.failure_type !== "None" ? r.failure_type : "ANOMALY"}</span>
              <span className="anomaly-log-detail">
                torque {r.torque_nm}Nm · speed {r.rotational_speed_rpm}rpm ·
                air temp {r.air_temperature_c}°C · tool wear {r.tool_wear_min}min
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
