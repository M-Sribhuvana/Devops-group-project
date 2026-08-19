import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import ImageUploader from './components/ImageUploader';
import SamplePicker from './components/SamplePicker';
import DiagnosticResult from './components/DiagnosticResult';
import ChatWidget from './components/ChatWidget';
import { AlertCircle } from 'lucide-react';

export default function App() {
  const [backendStatus, setBackendStatus] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [resultData, setResultData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Healthcheck on mount
  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'healthy') {
          setBackendStatus(true);
        }
      })
      .catch((err) => {
        console.warn("Backend API offline or proxy disconnected", err);
        setBackendStatus(false);
      });
  }, []);

  // Handle file selection (drag-and-drop or file picker)
  const handleFileSelect = (file, customPreviewUrl = null) => {
    setSelectedFile(file);
    setResultData(null);
    setErrorMessage(null);

    const url = customPreviewUrl || URL.createObjectURL(file);
    setPreviewUrl(url);

    // Auto trigger analysis
    analyzeImage(file);
  };

  const analyzeImage = async (file) => {
    setIsAnalyzing(true);
    setErrorMessage(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error (${response.status})`);
      }

      const json = await response.json();
      if (json.success) {
        setResultData(json);
      } else {
        throw new Error("Prediction failed");
      }
    } catch (err) {
      console.error("Diagnosis error:", err);
      setErrorMessage("Could not connect to FastAPI server on port 8000. Ensure backend server is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResultData(null);
    setErrorMessage(null);
  };

  return (
    <div className="app-container">
      <Navbar backendStatus={backendStatus} />

      <HeroSection />

      {errorMessage && (
        <div style={{
          background: 'rgba(212, 67, 51, 0.08)',
          border: '1px solid rgba(212, 67, 51, 0.3)',
          color: '#D44333',
          padding: '0.85rem 1.4rem',
          borderRadius: 'var(--radius-full)',
          margin: '0 auto 1.8rem auto',
          maxWidth: '650px',
          textAlign: 'center',
          fontSize: '0.86rem',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.5rem'
        }}>
          <AlertCircle size={16} />
          <span>{errorMessage}</span>
        </div>
      )}

      <main className="main-grid">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
          <ImageUploader
            selectedImage={selectedFile}
            previewUrl={previewUrl}
            isAnalyzing={isAnalyzing}
            onFileSelect={handleFileSelect}
            onReset={handleReset}
          />

          <SamplePicker onSelectSample={handleFileSelect} />
        </div>

        <div>
          <DiagnosticResult resultData={resultData} />
        </div>
      </main>

      <ChatWidget activeDiagnosis={resultData?.data} />
    </div>
  );
}
