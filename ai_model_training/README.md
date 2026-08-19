# AI Crop Health Assister — Model Training

Computer-vision training pipeline for **v1 crop health classification**.

- **Dataset:** [BrandonFors/Plant-Diseases-PlantVillage-Dataset](https://huggingface.co/datasets/BrandonFors/Plant-Diseases-PlantVillage-Dataset)
- **Crops:** Tomato, Potato, Corn (maize), Apple, Grape
- **Classes:** 25 exact PlantVillage folder names (see `crop_classes.py`)
- **Backbone:** MobileNetV2 (ImageNet), transfer learning, input **224×224** RGB
- **Splits:** stratified **70% / 15% / 15%** train / validation / test, seed **42**

Folder names on disk are the **exact** dataset strings (including spaces and trailing underscores). Do not rename them to short ids in this pipeline; the checkpoint stores `classes` and `class_to_idx` from `ImageFolder`.

---

## Files

| File | Role |
|------|------|
| `crop_classes.py` | Allow-list of the 25 class names |
| `data_prep.py` | Download Hugging Face data, filter, stratified split, write ImageFolder tree |
| `train_model.py` | Train MobileNetV2, save best-val checkpoint + mapping, evaluate test |
| `requirements.txt` | Python dependencies |

---

## Dataset layout after preparation

```
ai_model_training/dataset/
├── train/<PlantVillage class name>/*.jpg
├── val/<PlantVillage class name>/*.jpg
└── test/<PlantVillage class name>/*.jpg
```

All three splits contain the same 25 labels.

---

## Checkpoint format

Training writes `./checkpoints/crop_health_mobilenetv2.pth` with:

```python
{
    "state_dict": model.state_dict(),
    "classes": classes,          # list; index = model output argmax
    "class_to_idx": class_to_idx,
    "num_classes": num_classes,  # 25, taken from the dataset
}
```

**Classifier head (training and future inference must match):**

```python
model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    num_classes,
)
```

The backend is not updated yet. After training, load this checkpoint and use `checkpoint["classes"][pred_idx]` — do not assume a handwritten class list.

---

## Local run (from this folder)

```bash
cd ai_model_training
pip install -r requirements.txt
python data_prep.py
python train_model.py
```

Optional: if you already have a directory of the **exact** 25 class folders (not the old Kaggle fruit subset):

```bash
python data_prep.py --source-dir /path/to/plantvillage_class_folders
```

---

## Google Colab

1. Runtime → Change runtime type → **GPU** (T4 is enough). CPU works but is slow.
2. New notebook:

```python
from google.colab import drive
drive.mount("/content/drive")  # optional, to keep the checkpoint
```

3. Put this repo on the VM (clone, upload, or Drive copy), then:

```python
import os
os.chdir("/content/crop-doctor-ai/ai_model_training")  # adjust to your path

# Colab already has PyTorch. Install the rest:
!pip install -q datasets scikit-learn

!python data_prep.py
# writes ./dataset/{train,val,test}/...  (several minutes; ~31k images)

!python train_model.py --epochs 10 --batch-size 32
# writes ./checkpoints/crop_health_mobilenetv2.pth
```

4. Copy the checkpoint somewhere durable, for example Drive:

```python
import shutil
shutil.copy(
    "checkpoints/crop_health_mobilenetv2.pth",
    "/content/drive/MyDrive/crop_health_mobilenetv2.pth",
)
```

Do not point this script at `backend/fruit_disease_mobilenetv2.pth` until the backend is updated to load the new checkpoint dict and 25-class head.

### Colab notes

- First `data_prep.py` run downloads the Hugging Face dataset into the HF cache, then filters to 25 classes.
- `num_workers` is 2 on Linux+GPU (Colab) and 0 on Windows or CPU.
- `train_model.py` falls back to CPU if CUDA is unavailable.

---

## Flow

```
Hugging Face PlantVillage (38 classes)
        │  data_prep.py  (allow-list + 70/15/15 seed 42)
        ▼
dataset/{train,val,test}/<25 exact class names>
        │  train_model.py  (ImageFolder → num_classes, same mapping)
        ▼
MobileNetV2  classifier[1] = Linear(in_features, num_classes)
        │  keep best validation epoch
        ▼
checkpoints/crop_health_mobilenetv2.pth
  state_dict + classes + class_to_idx + num_classes
        │  later (not in this change)
        ▼
backend inference using checkpoint["classes"]
```
