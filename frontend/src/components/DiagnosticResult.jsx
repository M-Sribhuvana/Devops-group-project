import React, { useState } from 'react';
import { Activity, ShieldAlert, Leaf, TestTube, CheckCircle2, AlertTriangle, Droplets, Info, Sparkles } from 'lucide-react';

export default function DiagnosticResult({ resultData }) {
  const [activeTab, setActiveTab] = useState('symptoms');

  if (!resultData) {
    return (
      <div className="glass-card result-panel" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div style={{
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          background: 'var(--bg-canvas-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1.2rem auto',
          color: 'var(--accent-terracotta)'
        }}>
          <Activity size={32} />
        </div>
        <h3 style={{ fontSize: '1.25rem', color: 'var(--primary-forest)', fontWeight: 700 }}>
          Awaiting Leaf Specimen
        </h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '380px', margin: '0.6rem auto 0 auto', lineHeight: 1.5 }}>
          Upload a crop leaf photograph or select a sample specimen on the left to run deep learning disease classification.
        </p>
      </div>
    );
  }

  const { prediction, confidence_score, inference_mode, top_probabilities } = resultData.data;

  return (
    <div className="glass-card result-panel">
      {/* Header Info Card */}
      <div className="result-header-card">
        <div>
          <div className="result-crop-name">{prediction.crop_type}</div>
          <h2 className="result-disease-name">{prediction.display_name}</h2>
          {prediction.scientific_name !== 'N/A' && (
            <div style={{ fontSize: '0.82rem', fontStyle: 'italic', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
              {prediction.scientific_name}
            </div>
          )}
          <div style={{ marginTop: '0.6rem' }}>
            <span className={`severity-pill severity-${prediction.severity}`}>
              <AlertTriangle size={13} />
              Severity: {prediction.severity}
            </span>
          </div>
        </div>

        <div className="confidence-ring">
          <div className="confidence-score">{confidence_score}%</div>
          <div className="confidence-label">Confidence</div>
        </div>
      </div>

      {/* Probability Breakdown */}
      <div className="predictions-box">
        <div className="predictions-title">
          Model Inference Breakdown ({inference_mode}):
        </div>
        {top_probabilities.map((item, idx) => (
          <div key={idx} className={`prediction-row ${idx === 0 ? 'active' : ''}`}>
            <span>{item.display_name}</span>
            <span style={{ fontWeight: 700 }}>{item.confidence}%</span>
          </div>
        ))}
      </div>

      {/* Rounded Pill Tabs Header */}
      <div className="tabs-header">
        <button
          className={`tab-btn ${activeTab === 'symptoms' ? 'active' : ''}`}
          onClick={() => setActiveTab('symptoms')}
        >
          Symptoms
        </button>
        <button
          className={`tab-btn ${activeTab === 'organic' ? 'active' : ''}`}
          onClick={() => setActiveTab('organic')}
        >
          Organic Remedy
        </button>
        <button
          className={`tab-btn ${activeTab === 'chemical' ? 'active' : ''}`}
          onClick={() => setActiveTab('chemical')}
        >
          Chemical Control
        </button>
        <button
          className={`tab-btn ${activeTab === 'prevention' ? 'active' : ''}`}
          onClick={() => setActiveTab('prevention')}
        >
          Agronomy & Care
        </button>
      </div>

      {/* Tab Contents */}
      <div className="tab-content">
        {activeTab === 'symptoms' && (
          <ul className="treatment-list">
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.4rem', lineHeight: 1.5 }}>
              {prediction.description}
            </p>
            {prediction.symptoms.map((symptom, idx) => (
              <li key={idx} className="treatment-item">
                <Info size={16} color="#66826B" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{symptom}</span>
              </li>
            ))}
          </ul>
        )}

        {activeTab === 'organic' && (
          <ul className="treatment-list">
            {prediction.organic_remedies.map((remedy, idx) => (
              <li key={idx} className="treatment-item organic">
                <Leaf size={16} color="#66826B" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{remedy}</span>
              </li>
            ))}
          </ul>
        )}

        {activeTab === 'chemical' && (
          <ul className="treatment-list">
            {prediction.chemical_treatments.map((treatment, idx) => (
              <li key={idx} className="treatment-item chemical">
                <TestTube size={16} color="#3A7BBF" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{treatment}</span>
              </li>
            ))}
          </ul>
        )}

        {activeTab === 'prevention' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
            <ul className="treatment-list">
              {prediction.prevention.map((prev, idx) => (
                <li key={idx} className="treatment-item prevention">
                  <CheckCircle2 size={16} color="#D96B27" style={{ flexShrink: 0, marginTop: '2px' }} />
                  <span>{prev}</span>
                </li>
              ))}
            </ul>

            <div style={{
              background: 'var(--bg-accent-soft)',
              padding: '1rem 1.2rem',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-terracotta)',
              fontSize: '0.86rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', color: 'var(--accent-terracotta)', fontWeight: 700, marginBottom: '0.3rem' }}>
                <Droplets size={15} /> Irrigation & Soil Protocol:
              </div>
              <p style={{ color: 'var(--text-secondary)' }}>{prediction.recommended_irrigation}</p>
              <p style={{ color: 'var(--primary-forest)', marginTop: '0.4rem', fontWeight: 600, fontSize: '0.82rem' }}>
                🌱 <strong>NPK Guidance:</strong> {prediction.npk_fertilizer_tip}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
