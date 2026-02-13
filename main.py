"""
Text-to-Speech API with Translation
FIXED VERSION - Added Form(...) annotations for file upload
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
import hashlib
from typing import Optional
import PyPDF2
import docx
from gtts import gTTS
from deep_translator import GoogleTranslator

# ================== APP SETUP ==================

app = FastAPI(
    title="Text-to-Speech API with Translation",
    version="2.1.1",
    description="Convert text to speech with automatic translation support"
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

# ================== LANGUAGES ==================

LANGUAGE_NAME_TO_CODE = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "japanese": "ja",
    "korean": "ko",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "hindi": "hi",
    "arabic": "ar",
    "dutch": "nl",
    "polish": "pl",
    "turkish": "tr",
    "bengali": "bn",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur",
    "vietnamese": "vi",
    "thai": "th",
    "indonesian": "id",
    "malay": "ms",
    "persian": "fa",
    "hebrew": "he",
    "swahili": "sw",
}

VALID_CODES = set(LANGUAGE_NAME_TO_CODE.values())


def normalize_language(lang: Optional[str]) -> Optional[str]:
    if not lang:
        return None

    lang = lang.strip().lower()

    if lang in LANGUAGE_NAME_TO_CODE:
        return LANGUAGE_NAME_TO_CODE[lang]

    if lang in VALID_CODES:
        return lang

    raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")

# ================== HELPERS ==================

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    if source_lang == target_lang:
        return text

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def generate_audio_filename(text: str, custom_name: Optional[str] = None) -> str:
    if custom_name:
        base = custom_name.replace(" ", "_")
    else:
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"speech_{timestamp}_{text_hash}"

    return f"{base}.mp3"


def text_to_speech(text: str, output_path: str, target_language: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    tts = gTTS(text=text, lang=target_language, slow=False)
    tts.save(output_path)

# ================== ENDPOINTS ==================

@app.get("/")
def root():
    return {
        "message": "Text-to-Speech API with Translation",
        "version": "2.1.1"
    }


@app.get("/languages")
def get_languages():
    return {
        "supported_languages": {
            code: name.title()
            for name, code in LANGUAGE_NAME_TO_CODE.items()
        }
    }


@app.post("/tts/text", response_model=TTSResponse)
def convert_text_to_speech(input_data: TextInput, api_key: str = Depends(verify_api_key)):
    original_text = input_data.text
    final_text = original_text
    translation_applied = False

    target_language = normalize_language(input_data.target_language)
    source_language = normalize_language(input_data.translate_from)

    if source_language and source_language != target_language:
        final_text = translate_text(original_text, source_language, target_language)
        translation_applied = True

    audio_filename = generate_audio_filename(final_text, input_data.filename)
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)

    text_to_speech(final_text, audio_path, target_language)

    return TTSResponse(
        success=True,
        message="Speech generated successfully" if not translation_applied
        else f"Text translated from {source_language} to {target_language} and speech generated successfully",
        audio_file=audio_filename,
        file_path=f"/audio/{audio_filename}",
        generated_at=datetime.now().isoformat(),
        original_text=original_text if translation_applied else None,
        translated_text=final_text if translation_applied else None,
        translation_applied=translation_applied
    )


@app.post("/tts/file", response_model=TTSResponse)
async def convert_file_to_speech(
    file: UploadFile = File(...),
    custom_filename: Optional[str] = Form(None),
    target_language: str = Form("en"),
    translate_from: Optional[str] = Form(None),
    api_key: str = Depends(verify_api_key)
):
    target_language = normalize_language(target_language)
    source_language = normalize_language(translate_from)

    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        ext = file.filename.lower().split(".")[-1]

        if ext == "pdf":
            text = extract_text_from_pdf(temp_file_path)
        elif ext in ["docx", "doc"]:
            text = extract_text_from_docx(temp_file_path)
        elif ext == "txt":
            with open(temp_file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in file")

        if len(text) > 5000:
            text = text[:5000]

        original_text = text
        final_text = text
        translation_applied = False

        if source_language and source_language != target_language:
            final_text = translate_text(original_text, source_language, target_language)
            translation_applied = True

        audio_filename = generate_audio_filename(final_text, custom_filename)
        audio_path = os.path.join(OUTPUT_DIR, audio_filename)

        text_to_speech(final_text, audio_path, target_language)

        return TTSResponse(
            success=True,
            message="Speech generated successfully"
            if not translation_applied
            else f"File translated from {source_language} to {target_language} and speech generated successfully",
            audio_file=audio_filename,
            file_path=f"/audio/{audio_filename}",
            generated_at=datetime.now().isoformat(),
            original_text=original_text[:200] if translation_applied else None,
            translated_text=final_text[:200] if translation_applied else None,
            translation_applied=translation_applied
        )

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.get("/audio/{filename}")
def download_audio(filename: str, api_key: str = Depends(verify_api_key)):
    path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path, media_type="audio/mpeg", filename=filename)


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.1.1"}
