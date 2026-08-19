import React from 'react';
import { Sparkles, Leaf, ShieldCheck, Sun } from 'lucide-react';
import heroPlantImg from '../assets/hero-plant.jpg';

export default function HeroSection() {
  const crops = [
    { name: 'Wheat', scientific: 'Triticum aestivum', icon: '🌾' },
    { name: 'Rice', scientific: 'Oryza sativa', icon: '🌼' },
    { name: 'Corn / Maize', scientific: 'Zea mays', icon: '🌽' },
    { name: 'Tomato', scientific: 'Solanum lycopersicum', icon: '🍅' },
    { name: 'Potato', scientific: 'Solanum tuberosum', icon: '🥔' },
    { name: 'Cotton', scientific: 'Gossypium hirsutum', icon: '🌱' },
    { name: 'Soybean', scientific: 'Glycine max', icon: '🌿' },
    { name: 'Apple', scientific: 'Malus domestica', icon: '🍎' },
    { name: 'Grape', scientific: 'Vitis vinifera', icon: '🍇' },
  ];

  return (
    <section className="hero-section">
      {/* 3D Botanical Hero Image Card */}
      <div className="hero-visual-card">
        <div className="hero-3d-plant-wrapper">
          <img
            src={heroPlantImg}
            alt="3D Botanical Specimen"
            className="hero-3d-plant-img"
          />
        </div>

        <div className="hero-pill">
          <Sparkles size={14} />
          <span>Deep Learning Computer Vision & Agricultural AI</span>
        </div>

        <h2 className="hero-title">
          Intelligent Crop Health & <span>Disease Diagnosis</span>
        </h2>

        <p className="hero-subtitle">
          Upload a specimen leaf photograph. Our MobileNetV2 neural vision network inspects pathology in real-time, delivering bespoke organic remedies, chemical protocols, and agronomic guidance.
        </p>

        <div className="crops-bar">
          {crops.map((crop, idx) => (
            <div key={idx} className="crop-tag" title={crop.scientific}>
              <span>{crop.icon}</span>
              <span>{crop.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
