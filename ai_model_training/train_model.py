"""
MobileNetV2 Transfer Learning Script for Fruit Crop Leaf Disease Classification
Author: Computer Science & Engineering (CSE) Student AI Module
Dataset: Kaggle PlantVillage (Fruit Crops Subset)
"""

import os
import time
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms

# 1. Configuration & Hyperparameters
DATA_DIR = "./dataset"  # Structure: dataset/train/<class_name>, dataset/val/<class_name>
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 16  # 16 Fruit Crop Healthy & Diseased Classes
SAVE_MODEL_PATH = "../backend/fruit_disease_mobilenetv2.pth"

# Target class labels matching backend definition
CLASS_NAMES = [
    "apple_scab", "apple_black_rot", "apple_cedar_rust", "apple_healthy",
    "grape_black_rot", "grape_esca", "grape_leaf_blight", "grape_healthy",
    "peach_bacterial_spot", "peach_healthy", "strawberry_leaf_scorch", "strawberry_healthy",
    "cherry_powdery_mildew", "cherry_healthy", "citrus_greening", "citrus_healthy"
]

def get_data_transforms():
    """Define data augmentation for training and normalization for validation."""
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    return data_transforms

def build_mobilenetv2_model(num_classes):
    """Load MobileNetV2 pretrained on ImageNet and replace final classification layer."""
    print("[CSE ML] Loading MobileNetV2 pretrained backbone...")
    model = models.mobilenet_v2(pretrained=True)

    # Freeze early convolutional layers for transfer learning efficiency
    for param in model.parameters():
        param.requires_grad = False

    # Unfreeze higher feature layers
    for param in model.features[14:].parameters():
        param.requires_grad = True

    # Replace classifier head
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes)
    )

    return model

def train_model(model, dataloaders, dataset_sizes, criterion, optimizer, scheduler, device, num_epochs=10):
    """Execute training loop, compute loss & accuracy, save best weights."""
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        print("-" * 30)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data batches
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                # Forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # Backward pass & optimization step in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} | Acc: {epoch_acc*100:.2f}%")

            # Deep copy best model weights
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

    time_elapsed = time.time() - since
    print(f"\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
    print(f"Best Validation Accuracy: {best_acc*100:.2f}%")

    # Load best model weights
    model.load_state_dict(best_model_wts)
    return model

def main():
    print("=" * 60)
    print("  CSE Student ML Training: Fruit Crop Disease Classifier")
    print("=" * 60)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using execution device: {device}")

    if not os.path.exists(DATA_DIR):
        print(f"\n[Error] Dataset directory '{DATA_DIR}' not found!")
        print("Please download PlantVillage Fruit subset into ./dataset/train and ./dataset/val")
        print("Refer to ai_model_training/README.md for dataset download instructions.\n")
        return

    data_transforms = get_data_transforms()
    image_datasets = {x: datasets.ImageFolder(os.path.join(DATA_DIR, x), data_transforms[x]) for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=4) for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

    model = build_mobilenetv2_model(NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LEARNING_RATE)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.1)

    print("\nStarting Training Pipeline...")
    trained_model = train_model(model, dataloaders, dataset_sizes, criterion, optimizer, exp_lr_scheduler, device, NUM_EPOCHS)

    # Save model weights for FastAPI backend server
    os.makedirs(os.path.dirname(SAVE_MODEL_PATH), exist_ok=True)
    torch.save(trained_model.state_dict(), SAVE_MODEL_PATH)
    print(f"\n✅ Model weights successfully saved to: {SAVE_MODEL_PATH}")

if __name__ == '__main__':
    main()
