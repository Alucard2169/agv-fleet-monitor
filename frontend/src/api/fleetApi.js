const API_BASE = "http://localhost:8000"

class ApiError extends Error {}

async function fetchJson(url, { retries = 2, timeoutMs = 4000 } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timer);
      if (!res.ok) throw new ApiError(`${res.status} ${res.statusText}`);
      return await res.json();
    } catch (err) {
      clearTimeout(timer);
      lastErr = err;
      if (attempt < retries) {
        await new Promise((r) => setTimeout(r, 400 * 2 ** attempt));
      }
    }
  }
  throw lastErr;
}

export async function fetchDevices() {
  return fetchJson(`${API_BASE}/devices`);
}

export async function fetchReadings(deviceId, limit = 50) {
  const rows = await fetchJson(`${API_BASE}/readings/${deviceId}?limit=${limit}`);
  return rows.map((r) => ({
    ...r,
    time: new Date(r.timestamp).toLocaleTimeString(),
    is_anomaly: r.is_anomaly === 1 || r.is_anomaly === true,
  }));
}
