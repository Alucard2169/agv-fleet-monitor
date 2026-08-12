export default function AnomalyDot({ cx, cy, payload }) {
  if (!payload?.is_anomaly) return null;
  return (
    <circle
      cx={cx}
      cy={cy}
      r={5}
      style={{ fill: "var(--status-critical)", stroke: "var(--status-critical)" }}
    />
  );
}
