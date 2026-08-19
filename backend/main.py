"""
FastAPI Backend Application for AI Crop Disease Detection
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fruit_diseases_db import FRUIT_DISEASE_DB, get_disease_by_id, list_all_crops
from model_inference import classifier, CLASS_NAMES
from llm_assistant import generate_chat_response

app = FastAPI(
    title="AI Crop Disease Detection API",
    description="Computer Vision & LLM Backend for Crop Leaf Disease Diagnosis and Care",
    version="1.0.0"
)

# Enable CORS for React Frontend (Vite default port 5173 / 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ChatRequest(BaseModel):
    prompt: str
    disease_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    source: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app_name": "AI Crop Disease Detection API",
        "crop_focus": "Crops (Wheat, Rice, Corn, Tomato, Potato, Cotton, Soybean, Apple, Grape and more)",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": classifier.is_trained_model_loaded,
        "inference_engine": "PyTorch MobileNetV2" if classifier.is_trained_model_loaded else "Computer Vision Feature Inspector",
        "supported_classes_count": len(CLASS_NAMES),
        "supported_crops": list_all_crops()
    }

@app.get("/api/fruit-crops")
def get_fruit_crops():
    return {
        "crops": list_all_crops(),
        "diseases_count": len(FRUIT_DISEASE_DB),
        "disease_database": FRUIT_DISEASE_DB
    }

@app.post("/api/predict")
async def predict_crop_disease(file: UploadFile = File(...)):
    """
    Accepts an uploaded fruit leaf image file, performs CV classification,
    and returns full diagnostic report with organic/chemical remedies.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded must be an image (JPEG, PNG, WEBP).")

    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        prediction_result = classifier.predict(contents, filename=file.filename)
        return {
            "success": True,
            "filename": file.filename,
            "data": prediction_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
def plant_assistant_chat(request: ChatRequest):
    """
    Handles user questions about plant care, treatments, and prevention,
    leveraging Gemini LLM API with agricultural fallback.
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        reply = generate_chat_response(
            prompt=request.prompt.strip(),
            disease_context=request.disease_context
        )
        api_key_present = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
        return ChatResponse(
            response=reply,
            source="Gemini 2.5 Flash" if api_key_present else "Fruit Crop Expert System"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot service error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
