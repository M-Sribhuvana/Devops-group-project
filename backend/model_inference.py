"""
MobileNetV2 inference engine for the trained 25-class PlantVillage model.
"""

from __future__ import annotations

import io
import os

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

from fruit_diseases_db import get_disease_by_id


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "ai_model_training",
        "checkpoints",
        "crop_health_mobilenetv2.pth",
    )
)

TARGET_IMAGE_SIZE = 224


# ============================================================
# CLASSIFIER
# ============================================================

class CropDiseaseClassifier:

    def __init__(self, model_path: str = MODEL_PATH):

        self.model_path = model_path
        self.model = None
        self.classes = []
        self.class_to_idx = {}
        self.is_trained_model_loaded = False

        # Same preprocessing used during validation/test
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225],
            ),
        ])

        self._load_model()

    # ========================================================
    # LOAD MODEL
    # ========================================================

    def _load_model(self):

        if not os.path.exists(self.model_path):

            print(
                f"[AI Model] Model not found: "
                f"{self.model_path}"
            )

            return

        try:

            print(
                f"[AI Model] Loading model from: "
                f"{self.model_path}"
            )

            checkpoint = torch.load(
                self.model_path,
                map_location="cpu",
            )

            # Read class information saved during training
            self.classes = checkpoint["classes"]
            self.class_to_idx = checkpoint["class_to_idx"]
            num_classes = checkpoint["num_classes"]

            print(
                f"[AI Model] Number of classes: "
                f"{num_classes}"
            )

            # ------------------------------------------------
            # Recreate MobileNetV2
            # ------------------------------------------------

            model = models.mobilenet_v2(
                weights=None
            )

            # Replace ImageNet classifier with our 25-class head
            in_features = model.classifier[1].in_features

            model.classifier[1] = nn.Linear(
                in_features,
                num_classes,
            )

            # Load trained weights
            model.load_state_dict(
                checkpoint["state_dict"]
            )

            model.eval()

            self.model = model
            self.is_trained_model_loaded = True

            print(
                "[AI Model] Successfully loaded "
                "trained MobileNetV2 model."
            )

            print("[AI Model] Classes:")

            for index, class_name in enumerate(self.classes):
                print(
                    f"  {index}: {class_name}"
                )

        except Exception as e:

            print(
                f"[AI Model] Failed to load model: {e}"
            )

            self.model = None
            self.is_trained_model_loaded = False

    # ========================================================
    # PREDICTION
    # ========================================================

    def predict(
        self,
        image_bytes: bytes,
        filename: str = "",
    ) -> dict:

        if not self.is_trained_model_loaded:

            raise RuntimeError(
                "Trained AI model is not loaded."
            )

        # ----------------------------------------------------
        # Open uploaded image
        # ----------------------------------------------------

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        original_width, original_height = image.size

        # ----------------------------------------------------
        # Preprocess
        # ----------------------------------------------------

        tensor = self.transform(image).unsqueeze(0)

        # ----------------------------------------------------
        # Model inference
        # ----------------------------------------------------

        with torch.no_grad():

            outputs = self.model(tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )[0]

        # ----------------------------------------------------
        # Best prediction
        # ----------------------------------------------------

        confidence, predicted_index = torch.max(
            probabilities,
            dim=0,
        )

        predicted_index = int(
            predicted_index.item()
        )

        confidence = float(
            confidence.item()
        )

        predicted_class = self.classes[
            predicted_index
        ]

        # ----------------------------------------------------
        # Top 3 predictions
        # ----------------------------------------------------

        top_values, top_indices = torch.topk(
            probabilities,
            k=min(3, len(self.classes)),
        )

        top_predictions = []

        for probability, index in zip(
            top_values.tolist(),
            top_indices.tolist(),
        ):

            class_name = self.classes[index]

            disease_id = self.convert_class_to_id(
                class_name
            )

            disease_info = get_disease_by_id(
                disease_id
            )

            top_predictions.append({
                "class_name": class_name,
                "class_id": disease_id,
                "display_name": disease_info.get(
                    "display_name",
                    class_name,
                ),
                "confidence": round(
                    probability * 100,
                    2,
                ),
            })

        # ----------------------------------------------------
        # Main disease information
        # ----------------------------------------------------

        disease_id = self.convert_class_to_id(
            predicted_class
        )

        disease_info = get_disease_by_id(
            disease_id
        )

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        return {

            "prediction": disease_info,

            "predicted_class": predicted_class,

            "confidence_score": round(
                confidence * 100,
                2,
            ),

            "inference_mode":
                "PyTorch MobileNetV2",

            "top_probabilities":
                top_predictions,

            "image_specs": {

                "dimensions":
                    f"{original_width}x{original_height} px",

                "processed_size":
                    "224x224 px",

                "color_mode":
                    image.mode,
            },
        }

    # ========================================================
    # CLASS NAME → DATABASE ID
    # ========================================================

    @staticmethod
    def convert_class_to_id(
        class_name: str
    ) -> str:

        mapping = {

            # ---------------- APPLE ----------------

            "Apple___Apple_scab":
                "apple_scab",

            "Apple___Black_rot":
                "apple_black_rot",

            "Apple___Cedar_apple_rust":
                "apple_cedar_rust",

            "Apple___healthy":
                "apple_healthy",


            # ---------------- CORN ----------------

            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot":
                "corn_cercospora_leaf_spot",

            "Corn_(maize)___Common_rust_":
                "corn_common_rust",

            "Corn_(maize)___Northern_Leaf_Blight":
                "corn_northern_leaf_blight",

            "Corn_(maize)___healthy":
                "corn_healthy",


            # ---------------- GRAPE ----------------

            "Grape___Black_rot":
                "grape_black_rot",

            "Grape___Esca_(Black_Measles)":
                "grape_esca",

            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)":
                "grape_leaf_blight",

            "Grape___healthy":
                "grape_healthy",


            # ---------------- POTATO ----------------

            "Potato___Early_blight":
                "potato_early_blight",

            "Potato___Late_blight":
                "potato_late_blight",

            "Potato___healthy":
                "potato_healthy",


            # ---------------- TOMATO ----------------

            "Tomato___Bacterial_spot":
                "tomato_bacterial_spot",

            "Tomato___Early_blight":
                "tomato_early_blight",

            "Tomato___Late_blight":
                "tomato_late_blight",

            "Tomato___Leaf_Mold":
                "tomato_leaf_mold",

            "Tomato___Septoria_leaf_spot":
                "tomato_septoria_leaf_spot",

            "Tomato___Spider_mites Two-spotted_spider_mite":
                "tomato_spider_mites",

            "Tomato___Target_Spot":
                "tomato_target_spot",

            "Tomato___Tomato_Yellow_Leaf_Curl_Virus":
                "tomato_yellow_leaf_curl_virus",

            "Tomato___Tomato_mosaic_virus":
                "tomato_mosaic_virus",

            "Tomato___healthy":
                "tomato_healthy",
        }

        return mapping.get(
            class_name,
            class_name.lower().replace(
                "___",
                "_",
            ),
        )


# ============================================================
# GLOBAL CLASSIFIER
# ============================================================

classifier = CropDiseaseClassifier()


# main.py imports this
CLASS_NAMES = classifier.classes