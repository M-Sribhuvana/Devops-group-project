# AI Crop Health Assessor - CSE Student Model Training Guide

This module contains the Computer Vision model training code for the **Fruit Crop Health Assessor** project.

## 📌 Model Architecture Overview
- **Backbone**: `MobileNetV2` (Pretrained on ImageNet)
- **Technique**: Transfer Learning & Fine-tuning
- **Input Resolution**: 224 × 224 RGB pixels
- **Classes (16 Fruit Crop Pathology Labels)**:
  - **Apple**: Apple Scab, Black Rot, Cedar Apple Rust, Healthy
  - **Grape**: Black Rot, Esca (Black Measles), Leaf Blight, Healthy
  - **Peach**: Bacterial Spot, Healthy
  - **Strawberry**: Leaf Scorch, Healthy
  - **Cherry**: Powdery Mildew, Healthy
  - **Citrus / Orange**: Huanglongbing (Citrus Greening), Healthy

---

## 🚀 How to Train Your Model (Step-by-Step)

### Step 1: Install Dependencies
```bash
pip install torch torchvision numpy pillow
```

### Step 2: Download PlantVillage Fruit Dataset
1. Visit Kaggle: [PlantVillage Dataset on Kaggle](https://www.kaggle.com/datasets/emware/plantvillage-fruit-crops)
2. Download and extract the fruit crop image subfolders into `ai_model_training/dataset/`:
```
ai_model_training/
└── dataset/
    ├── train/
    │   ├── apple_scab/
    │   ├── grape_black_rot/
    │   └── ...
    └── val/
        ├── apple_scab/
        ├── grape_black_rot/
        └── ...
```

### Step 3: Run Training Script
```bash
python train_model.py
```

### Step 4: Export to FastAPI Backend
Upon training completion, `train_model.py` automatically exports the trained PyTorch weights to:
```
../backend/fruit_disease_mobilenetv2.pth
```
When you restart your FastAPI backend server (`python main.py`), it will automatically detect and load your trained `.pth` model weights for live inferences!
