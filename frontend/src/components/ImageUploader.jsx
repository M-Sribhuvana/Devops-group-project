import React, { useRef } from 'react';
import { UploadCloud, Image as ImageIcon, RotateCcw, Zap, Sparkles } from 'lucide-react';

export default function ImageUploader({ selectedImage, previewUrl, isAnalyzing, onFileSelect, onReset }) {
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="glass-card">
      <div className="card-header">
        <h3 className="card-title">
          <UploadCloud size={22} color="#D96B27" />
          <span>Specimen Leaf Inspection</span>
        </h3>

        {previewUrl && (
          <button onClick={onReset} className="btn-pill-secondary">
            <RotateCcw size={13} /> Reset
          </button>
        )}
      </div>

      {!previewUrl ? (
        <div
          className="dropzone"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="upload-icon-box">
            <ImageIcon size={32} />
          </div>
          <div className="dropzone-text">
            <h3>Drag & Drop Leaf Photograph</h3>
            <p>PNG, JPG, JPEG, WEBP • High-resolution supported</p>
          </div>
          <div style={{ marginTop: '1.2rem' }}>
            <span className="btn-pill-terracotta">
              Browse Files
            </span>
          </div>
          <input
            type="file"
            ref={fileInputRef}
            className="file-input"
            accept="image/*"
            onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])}
          />
        </div>
      ) : (
        <div className="scanner-container">
          <img src={previewUrl} alt="Crop Leaf Preview" className="scanner-image" />
          {isAnalyzing && <div className="scanner-beam" />}
          <div className="scanner-overlay">
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Zap size={16} color="#EB7E3D" />
              {isAnalyzing ? 'MobileNetV2 Neural Inspection Active...' : 'Diagnostic Scan Ready'}
            </span>
            <span style={{ fontSize: '0.78rem', opacity: 0.85, fontWeight: 500 }}>
              {selectedImage?.name || 'Selected Specimen'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
