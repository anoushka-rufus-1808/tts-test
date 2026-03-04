"""
Text-to-Speech API with Translation
FINAL VERSION - Switched to edge-tts for high reliability and better voices.
"""
import os
import hashlib
import json
import asyncio
import edge_tts
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import docx
from deep_translator import GoogleTranslator

# ================== APP SETUP ==================

app = FastAPI(
    title="Text-to-Speech API with Translation",
    version="3.0.0",
    description="High-reliability TTS using edge-tts"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY", "your-secret-api-key-12345")
OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================== AUTH ==================

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# ================== MODELS ==================

class TextInput(BaseModel):
    text: str
    filename: Optional[str] = None
    target_language: Optional[str] = "en"
    translate_from: Optional[str] = None

class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_file: str
    file_path: str
    generated_at: str
    original_text: Optional[str] = None
    translated_text: Optional[str] = None
    translation_applied: bool = False

# ================== HELPERS ==================

def normalize_language(lang: Optional[str]) -> str:
    if not lang: return "en"
    lang = lang.strip().lower()
    mapping = {"english": "en", "hindi": "hi", "en": "en", "hi": "hi"}
    return mapping.get(lang, "en")

async def text_to_speech_logic(text: str, output_path: str, lang_code: str):
    """Uses edge-tts for high-quality, reliable audio generation."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Select high-quality Neural voices
    voice_map = {
        "hi": "hi-IN-MadhurNeural",
        "en": "en-US-GuyNeural"
    }
    selected_voice = voice_map.get(lang_code, "en-US-GuyNeural")
    
    try:
        communicate = edge_tts.Communicate(text, selected_voice)
        await communicate.save(output_path)
    except Exception as e:
        print(f"Edge-TTS Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Audio generation failed.")

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if source_lang == target_lang: return text
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

def generate_audio_filename(text: str, custom_name: Optional[str] = None) -> str:
    if custom_name:
        base = custom_name.replace(" ", "_")
    else:
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"speech_{timestamp}_{text_hash}"
    return f"{base}.mp3"

# ================== ENDPOINTS ==================

@app.get("/")
def root():
    return {"message": "TTS API Live", "engine": "edge-tts"}

@app.post("/tts/text", response_model=TTSResponse)
async def convert_text_to_speech(input_data: TextInput, api_key: str = Depends(verify_api_key)):
    original_text = input_data.text
    final_text = original_text
    translation_applied = False

    target_lang = normalize_language(input_data.target_language)
    source_lang = normalize_language(input_data.translate_from) if input_data.translate_from else None

    if source_lang and source_lang != target_lang:
        final_text = translate_text(original_text, source_lang, target_lang)
        translation_applied = True

    audio_filename = generate_audio_filename(final_text, input_data.filename)
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)

    await text_to_speech_logic(final_text, audio_path, target_lang)

    return TTSResponse(
        success=True,
        message="Speech generated",
        audio_file=audio_filename,
        file_path=f"/audio/{audio_filename}",
        generated_at=datetime.now().isoformat(),
        original_text=original_text if translation_applied else None,
        translated_text=final_text if translation_applied else None,
        translation_applied=translation_applied
    )

@app.get("/audio/{filename}")
def download_audio(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="audio/mpeg")

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "edge-tts"}
