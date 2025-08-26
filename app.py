import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.pipeline.full_pipeline import upload_service
from src.logger import logging
from transformers import AutoModel
import whisper
from src.constants import INDIC_MODEL_NAME, WHISPER_MODEL_NAME
from src.entity.config_entity import ConfigEntity# Added import for ConfigEntity
import src.components.language_detector as lang_mod
import src.components.transcriber as trans_mod
app = FastAPI(
    title="Auto Caption Generator API",
    description="Video to Caption generation using IndicConformer + Whisper fallback for English",
    version="3.1.0"
)

# Ensure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

# In-memory storage
task_data = {}

# Global models
indic_model = None
whisper_model = None

@app.on_event("startup")
async def startup_event():
    global indic_model, whisper_model
    try:
        logging.info("Loading IndicConformer...")
        indic_model = AutoModel.from_pretrained(INDIC_MODEL_NAME, trust_remote_code=True)
        logging.info("Loading Whisper...")
        whisper_model = whisper.load_model(WHISPER_MODEL_NAME)
        # inject
        lang_mod.indic_model = indic_model
        lang_mod.whisper_model = whisper_model
        trans_mod.indic_model = indic_model
        trans_mod.whisper_model = whisper_model
        logging.info("Models loaded and injected into components")
    except Exception as e:
        logging.error(f"Model loading failed: {str(e)}")

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    global indic_model, whisper_model
    if not indic_model or not whisper_model:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    try:
        result = await upload_service(file, task_data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logging.error(f"Video upload error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {
        "message": "Auto Caption Generator API is running!",
        "models_loaded": bool(indic_model and whisper_model),
        "supported_languages": [f"{name} ({code})" for code, name in ConfigEntity().indic_languages.items()] + ["English (en)"]
    }





