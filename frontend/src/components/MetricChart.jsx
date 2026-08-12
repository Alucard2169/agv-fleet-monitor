import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import AnomalyDot from "./AnomalyDot";
import ChartSkeleton from "./ChartSkeleton";

export default function MetricChart({ title, dataKey, color, data, loading }) {
  return (
    <div className="chart-box">
      <h3>{title}</h3>
      {loading && data.length === 0 ? (
        <ChartSkeleton />
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={data}>
            <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
            <XAxis
              dataKey="time"
              tick={{ fill: "var(--text-tertiary)", fontSize: 11, fontFamily: "var(--font-mono)" }}
              minTickGap={30}
            />
            <YAxis tick={{ fill: "var(--text-tertiary)", fontSize: 11, fontFamily: "var(--font-mono)" }} />
            <Tooltip
              contentStyle={{
                background: "var(--surface-raised)",
                border: "1px solid var(--border-strong)",
                fontFamily: "var(--font-mono)",
                fontSize: 12,
              }}
              labelStyle={{ color: "var(--text-secondary)" }}
            />
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              dot={<AnomalyDot />}
              isAnimationActive={false}
              strokeWidth={1.75}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
