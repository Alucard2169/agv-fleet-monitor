export default function DeviceTabs({ devices, currentDevice, onSelect }) {
  if (devices.length === 0) return null;
  return (
    <nav className="device-tabs" aria-label="Devices">
      {devices.map((d) => (
        <button
          key={d}
          className={d === currentDevice ? "device-tab is-active" : "device-tab"}
          onClick={() => onSelect(d)}
          aria-current={d === currentDevice}
        >
          {d}
        </button>
      ))}
    </nav>
  );
}
