export default function ConnectionStatus({ connected }) {
  return (
    <div className={`connection-status ${connected ? "is-live" : "is-down"}`}>
      <span className="pulse-dot" />
      {connected ? "Live" : "Reconnecting…"}
    </div>
  );
}
