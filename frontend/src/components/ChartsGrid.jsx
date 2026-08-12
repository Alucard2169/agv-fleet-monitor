import MetricChart from "./MetricChart";

const METRICS = [
  { title: "Air Temperature (°C)", dataKey: "air_temperature_c", color: "#6C9EFF" },
  { title: "Process Temperature (°C)", dataKey: "process_temperature_c", color: "#FB923C" },
  { title: "Rotational Speed (rpm)", dataKey: "rotational_speed_rpm", color: "#22D3EE" },
  { title: "Torque (Nm)", dataKey: "torque_nm", color: "#C084FC" },
  { title: "Tool Wear (min)", dataKey: "tool_wear_min", color: "#F472B6" },
];

export default function ChartsGrid({ data, loading }) {
  return (
    <div className="charts-grid">
      {METRICS.map((m) => (
        <MetricChart key={m.dataKey} data={data} loading={loading} {...m} />
      ))}
    </div>
  );
}
