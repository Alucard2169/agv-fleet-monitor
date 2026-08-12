export default function EmptyState({ title, detail }) {
  return (
    <div className="empty-state">
      <div className="empty-state-title">{title}</div>
      {detail && <div className="empty-state-detail">{detail}</div>}
    </div>
  );
}
