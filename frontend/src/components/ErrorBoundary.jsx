import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("Dashboard render error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="empty-state">
          <div className="empty-state-title">Something broke in the dashboard</div>
          <div className="empty-state-detail">Reload the page. Check the console if it persists.</div>
        </div>
      );
    }
    return this.props.children;
  }
}
