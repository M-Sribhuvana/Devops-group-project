"""
Step 1: Data Preparation Script - Filter PlantVillage Dataset to Fruit Crops
Author: Computer Science & Engineering (CSE) Student AI Module
"""

import os
import shutil
import random

# Target Fruit Crop classes from PlantVillage dataset
FRUIT_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Citrus___Huanglongbing_(Citrus_greening)",
    "Citrus___healthy"
]

# Standardized short label map
CLASS_LABEL_MAP = {
    "Apple___Apple_scab": "apple_scab",
    "Apple___Black_rot": "apple_black_rot",
    "Apple___Cedar_apple_rust": "apple_cedar_rust",
    "Apple___healthy": "apple_healthy",
    "Grape___Black_rot": "grape_black_rot",
    "Grape___Esca_(Black_Measles)": "grape_esca",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "grape_leaf_blight",
    "Grape___healthy": "grape_healthy",
    "Peach___Bacterial_spot": "peach_bacterial_spot",
    "Peach___healthy": "peach_healthy",
    "Strawberry___Leaf_scorch": "strawberry_leaf_scorch",
    "Strawberry___healthy": "strawberry_healthy",
    "Cherry_(including_sour)___Powdery_mildew": "cherry_powdery_mildew",
    "Cherry_(including_sour)___healthy": "cherry_healthy",
    "Citrus___Huanglongbing_(Citrus_greening)": "citrus_greening",
    "Citrus___healthy": "citrus_healthy"
}

def filter_and_split_dataset(raw_dataset_dir: str, output_dir: str = "./dataset", train_ratio: float = 0.8):
    """
    Filters raw PlantVillage dataset down to fruit-crop subfolders
    and splits images into train (80%) and validation (20%) sets.
    """
    print("=" * 60)
    print(" Step 1: Data Preparation (Filtering Fruit Crops)")
    print("=" * 60)

    if not os.path.exists(raw_dataset_dir):
        print(f"[Error] Raw dataset path '{raw_dataset_dir}' not found!")
        print("Please point to your downloaded PlantVillage directory.")
        return

    train_dir = os.path.join(output_dir, "train")
    val_dir = os.path.join(output_dir, "val")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    total_images_processed = 0

    for original_folder in os.listdir(raw_dataset_dir):
        if original_folder in FRUIT_CLASSES or any(fc in original_folder for fc in ["Apple", "Grape", "Peach", "Strawberry", "Cherry", "Citrus"]):
            short_name = CLASS_LABEL_MAP.get(original_folder, original_folder.lower().replace("___", "_"))

            src_folder = os.path.join(raw_dataset_dir, original_folder)
            if not os.path.isdir(src_folder):
                continue

            dest_train_class = os.path.join(train_dir, short_name)
            dest_val_class = os.path.join(val_dir, short_name)

            os.makedirs(dest_train_class, exist_ok=True)
            os.makedirs(dest_val_class, exist_ok=True)

            images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            random.shuffle(images)

            split_idx = int(len(images) * train_ratio)
            train_images = images[:split_idx]
            val_images = images[split_idx:]

            for img in train_images:
                shutil.copy(os.path.join(src_folder, img), os.path.join(dest_train_class, img))
            for img in val_images:
                shutil.copy(os.path.join(src_folder, img), os.path.join(dest_val_class, img))

            count = len(images)
            total_images_processed += count
            print(f"  ✓ Processed class '{short_name}': {len(train_images)} train, {len(val_images)} val ({count} total)")

    print(f"\n✅ Data Preparation Complete! {total_images_processed} fruit crop leaf images split into '{output_dir}/train' and '{output_dir}/val'.\n")

if __name__ == '__main__':
    filter_and_split_dataset("./plantvillage_raw")
