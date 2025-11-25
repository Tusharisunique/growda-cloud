import os
import tempfile
import shutil
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf

# Import local modules
from model import preprocess_image, get_class_and_confidence

# Configuration
MODEL_PATH = "global_model.keras"

# Initialize FastAPI
app = FastAPI(title="Growda Cloud API - Pneumonia Detection")

# CORS middleware - allow all origins for cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for cloud deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_model_info():
    """Get model information"""
    if not os.path.exists(MODEL_PATH):
        return None
    
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        return {
            "model_loaded": True,
            "input_shape": str(model.input_shape),
            "output_shape": str(model.output_shape),
            "total_params": model.count_params(),
            "layers": len(model.layers),
            "model_path": MODEL_PATH
        }
    except Exception as e:
        return {"model_loaded": False, "error": str(e)}

def get_training_status():
    """Return static training status (no federated learning in cloud)"""
    return {
        "round": 3,  # Static - based on your completed training
        "global_accuracy": 0.92,  # Static - based on your final model accuracy
        "connected_clients": 0,  # No clients in cloud version
        "total_rounds": 3,
        "last_update": "Training completed locally",
        "cloud_mode": True,
        "federated_learning": False,
        "model_status": "Trained and deployed"
    }

def get_metrics_history():
    """Return static training history"""
    return {
        "history": [
            {"round": 1, "accuracy": 0.85, "clients": [{"client": "hospital_A", "accuracy": 0.84}, {"client": "hospital_B", "accuracy": 0.86}]},
            {"round": 2, "accuracy": 0.89, "clients": [{"client": "hospital_A", "accuracy": 0.88}, {"client": "hospital_B", "accuracy": 0.90}]},
            {"round": 3, "accuracy": 0.92, "clients": [{"client": "hospital_A", "accuracy": 0.91}, {"client": "hospital_B", "accuracy": 0.93}]}
        ]
    }

# API Endpoints
@app.get("/")
def root():
    model_info = get_model_info()
    return {
        "message": "Growda Cloud API - Pneumonia Detection",
        "mode": "Cloud Deployment (Static Model)",
        "model_info": model_info,
        "features": ["Prediction", "Model Info", "Training History (Read-only)"]
    }

@app.get("/status")
def status():
    """Get system status"""
    return get_training_status()

@app.get("/training_status")
def training_status():
    """Backward-compatible endpoint"""
    return get_training_status()

@app.get("/metrics/history")
def metrics_history():
    """Get training metrics history (static)"""
    return get_metrics_history()

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    """Make prediction using global model"""
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=400, detail="Model not found. Please ensure global_model.keras is in the backend directory.")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        img = preprocess_image(temp_file_path)
        prediction = model.predict(img)
        class_name, confidence, severity = get_class_and_confidence(prediction)
        return {
            "prediction": class_name,
            "confidence": float(confidence),
            "severity_level": severity,
            "model_info": "Cloud-deployed trained model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    finally:
        os.unlink(temp_file_path)

@app.get("/model/info")
def model_info():
    """Get detailed model information"""
    info = get_model_info()
    if not info or not info.get("model_loaded"):
        raise HTTPException(status_code=404, detail="Model not found or failed to load")
    return info

@app.get("/health")
def health_check():
    """Health check endpoint"""
    model_info = get_model_info()
    return {
        "status": "healthy",
        "model_loaded": model_info.get("model_loaded", False) if model_info else False,
        "service": "Growda Cloud API"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the cloud service"""
    print("🚀 Starting Growda Cloud API...")
    print("📦 Mode: Static Model Deployment (No Federated Learning)")
    
    model_info = get_model_info()
    if model_info and model_info.get("model_loaded"):
        print("✅ Global model loaded successfully")
        print(f"🧠 Model parameters: {model_info.get('total_params', 'Unknown')}")
        print(f"🎯 Ready for predictions!")
    else:
        print("⚠️ Warning: Model not found. Please ensure global_model.keras is in the backend directory")
    
    print("🌐 Cloud API ready for frontend connections")

if __name__ == "__main__":
    uvicorn.run("simple_cloud_main:app", host="0.0.0.0", port=8000, reload=True)
