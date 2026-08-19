"""
Prepare the Hugging Face PlantVillage dataset for 25-class crop health training.

Downloads BrandonFors/Plant-Diseases-PlantVillage-Dataset, keeps only the
allow-listed class names, and writes a stratified 70/15/15 ImageFolder layout.
"""

from __future__ import annotations

import argparse
import io
import os
import random
import shutil
import sys

from PIL import Image

from crop_classes import EXPECTED_NUM_CLASSES, HF_DATASET_ID, TARGET_CLASS_SET, TARGET_CLASSES

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
SPLITS = ("train", "val", "test")
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
DEFAULT_SEED = 42


def _is_image_file(name: str) -> bool:
    return name.lower().endswith(IMAGE_EXTENSIONS)


def _as_pil(image_obj) -> Image.Image:
    """Convert a Hugging Face image field (PIL, dict, or path) to RGB PIL."""
    if isinstance(image_obj, Image.Image):
        return image_obj.convert("RGB")
    if isinstance(image_obj, dict) and "bytes" in image_obj:
        return Image.open(io.BytesIO(image_obj["bytes"])).convert("RGB")
    if isinstance(image_obj, dict) and "path" in image_obj and image_obj["path"]:
        return Image.open(image_obj["path"]).convert("RGB")
    if isinstance(image_obj, (str, os.PathLike)):
        return Image.open(image_obj).convert("RGB")
    return Image.open(io.BytesIO(image_obj)).convert("RGB")


def _resolve_columns(features) -> tuple[str, str]:
    image_col = next((key for key in ("image", "img") if key in features), None)
    label_col = next(
        (key for key in ("label", "labels", "class", "disease") if key in features),
        None,
    )
    if image_col is None or label_col is None:
        raise ValueError(
            f"Could not find image/label columns in dataset features: {list(features.keys())}"
        )
    return image_col, label_col


def stratified_split_indices(n: int, seed: int, class_name: str) -> tuple[list[int], list[int], list[int]]:
    """Split n items 70/15/15 with remainder assigned to test. Requires n >= 3."""
    if n < 3:
        raise ValueError(
            f"Class '{class_name}' has only {n} images; need at least 3 for a 70/15/15 split."
        )

    order = list(range(n))
    random.Random(seed).shuffle(order)

    n_train = int(n * TRAIN_RATIO)
    n_val = int(n * VAL_RATIO)
    n_test = n - n_train - n_val

    if n_train < 1 or n_val < 1 or n_test < 1:
        n_train = max(1, n_train)
        n_val = max(1, n_val)
        n_test = n - n_train - n_val
        if n_test < 1:
            n_test = 1
            n_train = n - n_val - n_test

    train_idx = order[:n_train]
    val_idx = order[n_train : n_train + n_val]
    test_idx = order[n_train + n_val :]
    return train_idx, val_idx, test_idx


def _reset_output_dir(output_dir: str) -> None:
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    for split in SPLITS:
        for class_name in TARGET_CLASSES:
            os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)


def _print_split_summary(counts: dict[str, dict[str, int]], output_dir: str) -> None:
    print("\n" + "=" * 72)
    print(" Dataset summary")
    print("=" * 72)
    print(f"Number of classes: {EXPECTED_NUM_CLASSES}")
    print("Class names:")
    for class_name in TARGET_CLASSES:
        print(f"  - {class_name}")

    print("\nImages per class:")
    print(f"{'class':<55} {'total':>7} {'train':>7} {'val':>7} {'test':>7}")
    totals = {split: 0 for split in SPLITS}
    grand_total = 0
    missing = []
    for class_name in TARGET_CLASSES:
        per_split = counts[class_name]
        row_total = sum(per_split[split] for split in SPLITS)
        grand_total += row_total
        for split in SPLITS:
            totals[split] += per_split[split]
            if per_split[split] < 1:
                missing.append((class_name, split))
        print(
            f"{class_name:<55} {row_total:>7} {per_split['train']:>7} "
            f"{per_split['val']:>7} {per_split['test']:>7}"
        )

    print("-" * 72)
    print(
        f"{'TOTAL':<55} {grand_total:>7} {totals['train']:>7} "
        f"{totals['val']:>7} {totals['test']:>7}"
    )
    print(
        f"\nTrain/validation/test counts: "
        f"{totals['train']} / {totals['val']} / {totals['test']}"
    )
    print(f"Output directory: {os.path.abspath(output_dir)}")

    if missing:
        raise RuntimeError(
            "Every split must contain all 25 classes. Empty folders: "
            + ", ".join(f"{name} [{split}]" for name, split in missing)
        )

    print("\nAll 25 classes are present in train, val, and test.")


def _save_split_from_paths(class_name: str, files: list[str], split_indices: dict[str, list[int]], output_dir: str) -> dict[str, int]:
    written = {split: 0 for split in SPLITS}
    for split, indices in split_indices.items():
        dest_dir = os.path.join(output_dir, split, class_name)
        for i, rec_idx in enumerate(indices):
            dest = os.path.join(dest_dir, f"{split}_{i:06d}.jpg")
            with Image.open(files[rec_idx]) as img:
                img.convert("RGB").save(dest, format="JPEG", quality=95)
            written[split] += 1
    return written


def prepare_from_huggingface(output_dir: str, seed: int, dataset_id: str) -> dict[str, dict[str, int]]:
    try:
        from datasets import concatenate_datasets, load_dataset
    except ImportError as exc:
        raise SystemExit(
            "The `datasets` package is required. Install training deps with:\n"
            "  pip install -r requirements.txt"
        ) from exc

    print(f"Loading Hugging Face dataset: {dataset_id}")
    dataset_dict = load_dataset(dataset_id)
    parts = [dataset_dict[split_name] for split_name in dataset_dict]
    full = concatenate_datasets(parts) if len(parts) > 1 else parts[0]

    image_col, label_col = _resolve_columns(full.features)
    label_feature = full.features[label_col]
    class_names = getattr(label_feature, "names", None)
    print(f"Using columns image={image_col!r}, label={label_col!r}")
    print(f"Source rows (all original splits combined): {len(full)}")

    # Read labels only so we do not decode tens of thousands of images into RAM.
    grouped_indices: dict[str, list[int]] = {name: [] for name in TARGET_CLASSES}
    skipped = 0
    for row_idx, raw_label in enumerate(full[label_col]):
        if isinstance(raw_label, str):
            class_name = raw_label
        elif class_names is not None:
            class_name = class_names[int(raw_label)]
        else:
            class_name = str(raw_label)
        if class_name not in TARGET_CLASS_SET:
            skipped += 1
            continue
        grouped_indices[class_name].append(row_idx)

    print(f"Kept {sum(len(v) for v in grouped_indices.values())} images in the 25-class allow-list")
    print(f"Skipped {skipped} images from other PlantVillage classes")

    missing_source = [name for name, rows in grouped_indices.items() if not rows]
    if missing_source:
        raise RuntimeError(
            "Hugging Face dataset is missing allow-listed classes: " + ", ".join(missing_source)
        )

    counts = {}
    for class_index, class_name in enumerate(TARGET_CLASSES):
        row_ids = grouped_indices[class_name]
        train_idx, val_idx, test_idx = stratified_split_indices(
            len(row_ids), seed + class_index, class_name
        )
        split_indices = {"train": train_idx, "val": val_idx, "test": test_idx}
        written = {split: 0 for split in SPLITS}
        for split, local_indices in split_indices.items():
            dest_dir = os.path.join(output_dir, split, class_name)
            for i, local_i in enumerate(local_indices):
                example = full[row_ids[local_i]]
                dest = os.path.join(dest_dir, f"{split}_{i:06d}.jpg")
                _as_pil(example[image_col]).save(dest, format="JPEG", quality=95)
                written[split] += 1
        counts[class_name] = written
        print(
            f"  {class_name}: {len(row_ids)} total -> "
            f"{written['train']} train / {written['val']} val / {written['test']} test"
        )
    return counts


def prepare_from_local_folders(source_dir: str, output_dir: str, seed: int) -> dict[str, dict[str, int]]:
    """Optional path: a directory whose subfolders use the exact PlantVillage class names."""
    print(f"Preparing from local class folders: {source_dir}")
    found = {
        name for name in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, name))
    }
    missing = [name for name in TARGET_CLASSES if name not in found]
    extra = sorted(found - TARGET_CLASS_SET)
    if missing:
        raise RuntimeError("Local source is missing allow-listed folders: " + ", ".join(missing))
    if extra:
        print(f"Ignoring {len(extra)} non-allow-listed folders")

    counts = {}
    for class_index, class_name in enumerate(TARGET_CLASSES):
        src_folder = os.path.join(source_dir, class_name)
        files = [
            os.path.join(src_folder, name)
            for name in os.listdir(src_folder)
            if _is_image_file(name)
        ]
        train_idx, val_idx, test_idx = stratified_split_indices(
            len(files), seed + class_index, class_name
        )
        split_indices = {"train": train_idx, "val": val_idx, "test": test_idx}
        counts[class_name] = _save_split_from_paths(class_name, files, split_indices, output_dir)
        print(
            f"  {class_name}: {len(files)} total -> "
            f"{counts[class_name]['train']} train / "
            f"{counts[class_name]['val']} val / "
            f"{counts[class_name]['test']} test"
        )
    return counts


def prepare_dataset(output_dir: str = "./dataset", seed: int = DEFAULT_SEED, source_dir: str | None = None, dataset_id: str = HF_DATASET_ID) -> None:
    print("=" * 72)
    print(" Step 1: Data preparation (25-class PlantVillage allow-list)")
    print("=" * 72)
    print(f"Split: {int(TRAIN_RATIO*100)}/{int(VAL_RATIO*100)}/{int(TEST_RATIO*100)} stratified, seed={seed}")
    print(f"Allow-list size: {EXPECTED_NUM_CLASSES}")

    _reset_output_dir(output_dir)
    if source_dir:
        counts = prepare_from_local_folders(source_dir, output_dir, seed)
    else:
        counts = prepare_from_huggingface(output_dir, seed, dataset_id)
    _print_split_summary(counts, output_dir)
    print("\nData preparation complete.\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Prepare the 25-class Crop Health dataset.")
    parser.add_argument("--output-dir", default="./dataset", help="ImageFolder root (train/val/test).")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--source-dir",
        default=None,
        help="Optional local folder of exact PlantVillage class names. "
        "If omitted, the Hugging Face dataset is downloaded.",
    )
    parser.add_argument("--hf-dataset", default=HF_DATASET_ID)
    args = parser.parse_args(argv)
    prepare_dataset(
        output_dir=args.output_dir,
        seed=args.seed,
        source_dir=args.source_dir,
        dataset_id=args.hf_dataset,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
