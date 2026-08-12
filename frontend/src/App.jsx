import { useDevices } from "./hooks/useDevices";
import { useReadings } from "./hooks/useReadings";
import ErrorBoundary from "./components/ErrorBoundary";
import FleetHeader from "./components/FleetHeader";
import AnomalyFeed from "./components/AnomalyFeed";
import DeviceTabs from "./components/DeviceTabs";
import ChartsGrid from "./components/ChartsGrid";
import EmptyState from "./components/EmptyState";
import "./App.css";

export default function App() {
  const {
    devices, currentDevice, setCurrentDevice,
    connected: devicesConnected, loading: devicesLoading,
  } = useDevices();
  const { readings, loading: readingsLoading, connected: readingsConnected } = useReadings(currentDevice);

  const connected = devicesConnected && readingsConnected;
  const anomalies = readings.filter((r) => r.is_anomaly);

  return (
    <ErrorBoundary>
      <div className="app">
        <FleetHeader currentDevice={currentDevice} anomalyCount={anomalies.length} connected={connected} />
        <DeviceTabs devices={devices} currentDevice={currentDevice} onSelect={setCurrentDevice} />

        {devicesLoading ? (
          <EmptyState title="Connecting to fleet…" />
        ) : devices.length === 0 ? (
          <EmptyState title="No devices reporting" detail="Start the simulator to see live telemetry." />
        ) : (
          <>
            <ChartsGrid data={readings} loading={readingsLoading} />
            <AnomalyFeed anomalies={anomalies} />
          </>
        )}
      </div>
    </ErrorBoundary>
  );
}
