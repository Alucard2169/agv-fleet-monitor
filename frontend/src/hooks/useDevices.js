import { useState, useEffect, useCallback, useRef } from "react";
import { fetchDevices } from "../api/fleetApi";

export function useDevices(pollMs = 2000) {
  const [devices, setDevices] = useState([]);
  const [currentDevice, setCurrentDevice] = useState(null);
  const [connected, setConnected] = useState(true);
  const [loading, setLoading] = useState(true);
  const firstLoad = useRef(true);

  const load = useCallback(async () => {
    try {
      const data = await fetchDevices();
      setDevices(data);
      setCurrentDevice((prev) => prev || data[0] || null);
      setConnected(true);
    } catch {
      setConnected(false);
    } finally {
      if (firstLoad.current) {
        setLoading(false);
        firstLoad.current = false;
      }
    }
  }, []);

  useEffect(() => {
    load();
    const id = setInterval(load, pollMs);
    return () => clearInterval(id);
  }, [load, pollMs]);

  return { devices, currentDevice, setCurrentDevice, connected, loading };
}
