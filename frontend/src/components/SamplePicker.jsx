import React from 'react';
import { Sparkles, Sprout } from 'lucide-react';

// Refined SVG Data URIs matching the warm botanical aesthetic
const SAMPLE_LEAF_IMAGES = {
  wheat_rust: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><rect width='200' height='200' fill='%23ECE6D8'/><path d='M100 20 C108 80 110 140 100 180 C90 140 92 80 100 20 Z' fill='%232D543E'/><ellipse cx='80' cy='80' rx='22' ry='9' fill='%233A6B4F' transform='rotate(-30 80 80)'/><ellipse cx='120' cy='110' rx='22' ry='9' fill='%233A6B4F' transform='rotate(30 120 110)'/><circle cx='86' cy='74' r='6' fill='%23D96B27'/><circle cx='108' cy='95' r='5' fill='%23C85918'/><circle cx='96' cy='120' r='7' fill='%23D96B27'/><line x1='100' y1='20' x2='100' y2='180' stroke='%231C3628' stroke-width='2.5'/></svg>",
  corn_blight: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><rect width='200' height='200' fill='%23ECE6D8'/><path d='M60 180 C80 120 90 60 100 20 C110 60 120 120 140 180 Z' fill='%23284B37'/><path d='M65 140 Q100 130 135 140' stroke='%2366826B' stroke-width='2' fill='none'/><path d='M70 110 Q100 100 130 110' stroke='%2366826B' stroke-width='2' fill='none'/><rect x='75' y='95' width='50' height='10' fill='%23D96B27' opacity='0.75' rx='3'/><rect x='80' y='125' width='40' height='8' fill='%23B85217' opacity='0.7' rx='3'/><line x1='100' y1='20' x2='100' y2='180' stroke='%231C3628' stroke-width='3'/></svg>",
  tomato_curl: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><rect width='200' height='200' fill='%23ECE6D8'/><path d='M100 20 C140 55 150 130 110 175 C60 165 50 95 80 50 Z' fill='%23365C44'/><path d='M80 50 Q120 80 110 130' stroke='%231C3628' stroke-width='2' fill='none'/><path d='M95 65 Q130 90 120 120' stroke='%231C3628' stroke-width='1.5' fill='none'/><circle cx='105' cy='85' r='8' fill='%23D99B26' opacity='0.7'/><circle cx='118' cy='110' r='6' fill='%23D96B27' opacity='0.65'/><circle cx='92' cy='130' r='5' fill='%23D99B26' opacity='0.7'/></svg>",
  potato_blight: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'><rect width='200' height='200' fill='%23ECE6D8'/><path d='M100 20 C145 55 145 140 100 180 C55 140 55 55 100 20 Z' fill='%232D543E'/><path d='M75 70 Q100 65 125 70 Q130 100 120 130 Q100 140 80 130 Q70 100 75 70 Z' fill='%2312241A' opacity='0.85'/><circle cx='90' cy='90' r='5' fill='%23D96B27'/><circle cx='112' cy='105' r='6' fill='%23D96B27'/><circle cx='100' cy='120' r='5' fill='%23C85918'/><line x1='100' y1='20' x2='100' y2='180' stroke='%231C3628' stroke-width='2.5'/></svg>"
};

export default function SamplePicker({ onSelectSample }) {
  const samples = [
    { id: 'wheat_rust', name: 'Wheat Rust', crop: 'Wheat Crop', img: SAMPLE_LEAF_IMAGES.wheat_rust },
    { id: 'corn_blight', name: 'Corn Blight', crop: 'Maize Crop', img: SAMPLE_LEAF_IMAGES.corn_blight },
    { id: 'tomato_curl', name: 'Tomato Leaf Curl', crop: 'Tomato Crop', img: SAMPLE_LEAF_IMAGES.tomato_curl },
    { id: 'potato_blight', name: 'Potato Blight', crop: 'Potato Crop', img: SAMPLE_LEAF_IMAGES.potato_blight },
  ];

  const handleSampleClick = async (sample) => {
    const res = await fetch(sample.img);
    const blob = await res.blob();
    const file = new File([blob], `${sample.id}_sample.png`, { type: 'image/png' });
    onSelectSample(file, sample.img);
  };

  return (
    <div className="samples-wrapper">
      <div className="samples-title">
        <Sprout size={16} color="#D96B27" />
        <span>Quick Test with Specimen Library:</span>
      </div>
      <div className="samples-grid">
        {samples.map((sample) => (
          <div key={sample.id} className="sample-card" onClick={() => handleSampleClick(sample)}>
            <div className="sample-img-box">
              <img src={sample.img} alt={sample.name} />
            </div>
            <div className="sample-name">{sample.name}</div>
            <div className="sample-crop-label">{sample.crop}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
