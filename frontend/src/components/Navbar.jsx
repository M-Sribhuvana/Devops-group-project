import React from 'react';
import { Activity, Cpu, Sprout, Sparkles } from 'lucide-react';

export default function Navbar({ backendStatus }) {
  return (
    <header className="navbar">
      <div className="brand-logo">
        <div className="brand-icon">
          <Sprout size={24} color="#ffffff" strokeWidth={2.5} />
        </div>
        <div className="brand-text">
          <h1>Crop Doctor AI</h1>
          <span>Botanical Vision & Diagnostic Core</span>
        </div>
      </div>

      <div className="nav-badges">
        <div className={`status-badge ${backendStatus ? '' : 'accent'}`}>
          <div className="pulse-dot" style={{ backgroundColor: backendStatus ? '#2E9E5B' : '#D96B27', boxShadow: backendStatus ? '0 0 8px #2E9E5B' : '0 0 8px #D96B27' }}></div>
          <span>API: {backendStatus ? 'Online' : 'Connecting...'}</span>
        </div>

        <div className="status-badge" style={{ background: 'rgba(28, 54, 40, 0.06)', borderColor: 'rgba(28, 54, 40, 0.15)', color: '#1C3628' }}>
          <Cpu size={14} color="#D96B27" />
          <span>MobileNetV2</span>
        </div>
      </div>
    </header>
  );
}
