import { useState, useEffect, useCallback, useRef } from "react";
import { fetchReadings } from "../api/fleetApi";

export function useReadings(deviceId, pollMs = 2000) {
  const [readings, setReadings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(true);
  const firstLoad = useRef(true);

  const load = useCallback(async () => {
    if (!deviceId) return;
    try {
      const rows = await fetchReadings(deviceId);
      setReadings(rows);
      setConnected(true);
    } catch {
      setConnected(false); // keep last-known-good data visible, don't blank the charts
    } finally {
      if (firstLoad.current) {
        setLoading(false);
        firstLoad.current = false;
      }
    }
  }, [deviceId]);

  useEffect(() => {
    firstLoad.current = true;
    setLoading(true);
    load();
    const id = setInterval(load, pollMs);
    return () => clearInterval(id);
  }, [load, pollMs, deviceId]);

  return { readings, loading, connected };
}
