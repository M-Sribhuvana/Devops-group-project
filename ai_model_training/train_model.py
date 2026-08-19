"""
MobileNetV2 transfer learning for 25-class crop leaf disease classification.

Expects an ImageFolder tree from data_prep.py:
  dataset/train/<exact PlantVillage class name>/
  dataset/val/...
  dataset/test/...
"""

from __future__ import annotations

import argparse
import copy
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report, confusion_matrix
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms

from crop_classes import EXPECTED_NUM_CLASSES, TARGET_CLASSES

DATA_DIR = "./dataset"
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
SAVE_MODEL_PATH = "./checkpoints/crop_health_mobilenetv2.pth"
SPLITS = ("train", "val", "test")


def get_num_workers() -> int:
    """Colab/Linux can use workers; Windows and CPU fallback stay on the main process."""
    if os.name == "nt":
        return 0
    return 2 if torch.cuda.is_available() else 0


def get_data_transforms():
    """Define data augmentation for training and normalization for validation/test."""
    eval_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return {
        "train": transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(20),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]),
        "val": eval_transform,
        "test": eval_transform,
    }


def build_mobilenetv2_model(num_classes: int):
    """Load ImageNet MobileNetV2 and replace the final Linear layer only."""
    print("Loading MobileNetV2 pretrained backbone...")
    try:
        model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    except Exception:
        model = models.mobilenet_v2(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False

    for param in model.features[14:].parameters():
        param.requires_grad = True

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def save_checkpoint(path: str, model, classes: list[str], class_to_idx: dict[str, int]) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "classes": classes,
            "class_to_idx": class_to_idx,
            "num_classes": len(classes),
        },
        path,
    )


def count_images_per_class(dataset: datasets.ImageFolder, classes: list[str]) -> dict[str, int]:
    counts = {name: 0 for name in classes}
    for _, label_idx in dataset.samples:
        counts[classes[label_idx]] += 1
    return counts


def verify_split_classes(image_datasets: dict) -> None:
    expected = set(TARGET_CLASSES)
    train_classes = image_datasets["train"].classes
    train_mapping = image_datasets["train"].class_to_idx
    for split, dataset in image_datasets.items():
        found = set(dataset.classes)
        if found != expected:
            missing = sorted(expected - found)
            extra = sorted(found - expected)
            raise RuntimeError(
                f"{split} class set does not match the 25-class allow-list.\n"
                f"  missing: {missing}\n"
                f"  extra: {extra}"
            )
        if dataset.classes != train_classes or dataset.class_to_idx != train_mapping:
            raise RuntimeError(
                f"{split} class-to-index mapping does not match train. "
                "All splits must use the same 25 labels in the same order."
            )


def print_dataset_stats(image_datasets: dict, dataset_sizes: dict) -> None:
    classes = image_datasets["train"].classes
    print("\n" + "=" * 72)
    print(" Training dataset")
    print("=" * 72)
    print(f"Number of classes: {len(classes)}")
    print("Class names:")
    for name in classes:
        print(f"  - {name}")

    print("\nImages per class:")
    print(f"{'class':<55} {'train':>7} {'val':>7} {'test':>7}")
    per_split_counts = {split: count_images_per_class(image_datasets[split], classes) for split in SPLITS}
    for name in classes:
        print(
            f"{name:<55} {per_split_counts['train'][name]:>7} "
            f"{per_split_counts['val'][name]:>7} {per_split_counts['test'][name]:>7}"
        )
    print("-" * 72)
    print(
        f"{'TOTAL':<55} {dataset_sizes['train']:>7} "
        f"{dataset_sizes['val']:>7} {dataset_sizes['test']:>7}"
    )
    print(
        f"\nTrain/validation/test counts: "
        f"{dataset_sizes['train']} / {dataset_sizes['val']} / {dataset_sizes['test']}"
    )


def train_model(model, dataloaders, dataset_sizes, criterion, optimizer, scheduler, device, num_epochs, classes, class_to_idx, save_path):
    """Train, keep the best validation weights, and write that checkpoint."""
    since = time.time()
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        print("-" * 30)

        for phase in ("train", "val"):
            model.train() if phase == "train" else model.eval()
            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            if phase == "train":
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]
            print(f"{phase.capitalize()} Loss: {epoch_loss:.4f} | Acc: {epoch_acc * 100:.2f}%")

            if phase == "val" and epoch_acc >= best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                save_checkpoint(save_path, model, classes, class_to_idx)
                print(f"  Saved best validation checkpoint (acc={best_acc * 100:.2f}%) -> {save_path}")

    time_elapsed = time.time() - since
    print(f"\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
    print(f"Best validation accuracy: {best_acc * 100:.2f}%")
    model.load_state_dict(best_model_wts)
    save_checkpoint(save_path, model, classes, class_to_idx)
    return model, float(best_acc)


@torch.no_grad()
def evaluate_model(model, dataloader, device, classes, split_name: str) -> float:
    model.eval()
    y_true = []
    y_pred = []

    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        y_true.extend(labels.cpu().numpy().tolist())
        y_pred.extend(preds.cpu().numpy().tolist())

    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    accuracy = float((y_true_arr == y_pred_arr).mean()) if len(y_true_arr) else 0.0

    print("\n" + "=" * 72)
    print(f" {split_name.capitalize()} evaluation")
    print("=" * 72)
    print(f"{split_name.capitalize()} accuracy: {accuracy * 100:.2f}%")
    print(f"\n{split_name.capitalize()} classification report:")
    print(
        classification_report(
            y_true_arr,
            y_pred_arr,
            labels=list(range(len(classes))),
            target_names=classes,
            digits=4,
            zero_division=0,
        )
    )

    matrix = confusion_matrix(y_true_arr, y_pred_arr, labels=list(range(len(classes))))
    print(f"{split_name.capitalize()} confusion matrix (rows=true, cols=pred):")
    print("Index mapping:")
    for idx, name in enumerate(classes):
        print(f"  {idx:2d} -> {name}")
    np.set_printoptions(linewidth=200, threshold=np.inf)
    print(matrix)
    return accuracy


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train the 25-class MobileNetV2 crop health model.")
    parser.add_argument("--data-dir", default=DATA_DIR)
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--lr", type=float, default=LEARNING_RATE)
    parser.add_argument("--save-path", default=SAVE_MODEL_PATH)
    args = parser.parse_args(argv)

    print("=" * 72)
    print(" Crop Health Assister — MobileNetV2 training (25 classes)")
    print("=" * 72)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using execution device: {device}")
    if device.type == "cpu":
        print("CPU fallback is active. Training will work but will be slower than a Colab GPU.")

    for split in SPLITS:
        split_path = os.path.join(args.data_dir, split)
        if not os.path.isdir(split_path):
            print(f"\n[Error] Missing '{split_path}'.")
            print("Run data_prep.py first so dataset/train, dataset/val, and dataset/test exist.\n")
            return

    data_transforms = get_data_transforms()
    image_datasets = {
        split: datasets.ImageFolder(os.path.join(args.data_dir, split), data_transforms[split])
        for split in SPLITS
    }
    verify_split_classes(image_datasets)

    classes = image_datasets["train"].classes
    class_to_idx = image_datasets["train"].class_to_idx
    num_classes = len(classes)
    if num_classes != EXPECTED_NUM_CLASSES:
        raise RuntimeError(f"Expected {EXPECTED_NUM_CLASSES} classes, found {num_classes}.")

    num_workers = get_num_workers()
    dataloaders = {
        "train": torch.utils.data.DataLoader(
            image_datasets["train"],
            batch_size=args.batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=device.type == "cuda",
        ),
        "val": torch.utils.data.DataLoader(
            image_datasets["val"],
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=device.type == "cuda",
        ),
        "test": torch.utils.data.DataLoader(
            image_datasets["test"],
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=device.type == "cuda",
        ),
    }
    dataset_sizes = {split: len(image_datasets[split]) for split in SPLITS}
    print_dataset_stats(image_datasets, dataset_sizes)
    print(f"DataLoader workers: {num_workers}")

    model = build_mobilenetv2_model(num_classes).to(device)
    print(
        f"Classifier head: Linear({model.classifier[1].in_features} -> {num_classes}) "
        "replacing classifier[1] (not a nested Sequential)"
    )
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.1)

    print("\nStarting training pipeline...")
    trained_model, best_val_acc = train_model(
        model,
        dataloaders,
        dataset_sizes,
        criterion,
        optimizer,
        exp_lr_scheduler,
        device,
        args.epochs,
        classes,
        class_to_idx,
        args.save_path,
    )

    test_acc = evaluate_model(trained_model, dataloaders["test"], device, classes, "test")

    print("\n" + "=" * 72)
    print(" Run complete")
    print("=" * 72)
    print(f"Number of classes: {num_classes}")
    print(f"Best validation accuracy: {best_val_acc * 100:.2f}%")
    print(f"Test accuracy: {test_acc * 100:.2f}%")
    print(f"Checkpoint (best validation weights + class mapping): {os.path.abspath(args.save_path)}")
    print(
        "Load later with torch.load(...); use checkpoint['classes'][pred_idx] "
        "so inference matches training indices."
    )


if __name__ == "__main__":
    main(sys.argv[1:])
