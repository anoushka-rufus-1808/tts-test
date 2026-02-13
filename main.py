"""
Text-to-Speech API with Translation
A simple API that converts text to speech using Google Text-to-Speech (gTTS)
Now with automatic translation support!
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header
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

# Initialize FastAPI app
app = FastAPI(
    title="Text-to-Speech API with Translation",
    version="2.0.0",
    description="Convert text to speech with automatic translation support"
)

# CORS middleware - allows browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key from environment variable (secure for deployment)
API_KEY = os.getenv("API_KEY", "your-secret-api-key-12345")

# Create directories for storage
OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Print API key on startup (only for debugging)
if os.getenv("ENVIRONMENT") != "production":
    print(f"🔑 API Key: {API_KEY}")

print("✅ gTTS (Google Text-to-Speech) is ready!")
print("✅ Translation support enabled!")


# ============= AUTHENTICATION =============
def verify_api_key(x_api_key: str = Header(...)):
    """Verify the API key from request headers"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# ============= MODELS =============
class TextInput(BaseModel):
    """Model for plain text input"""
    text: str
    filename: Optional[str] = None
    language: Optional[str] = "en"  # Target language for audio
    translate_from: Optional[str] = None  # Source language (if translation needed)


class TTSResponse(BaseModel):
    """Response model for TTS generation"""
    success: bool
    message: str
    audio_file: str
    file_path: str
    generated_at: str
    original_text: Optional[str] = None  # Original text before translation
    translated_text: Optional[str] = None  # Translated text (if translation was done)
    translation_applied: bool = False  # Whether translation was applied

# ============= LANGUAGE NORMALIZATION =============

# Based on Google Translate supported languages
LANGUAGE_NAME_TO_CODE = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "azerbaijani": "az",
    "bengali": "bn",
    "bulgarian": "bg",
    "catalan": "ca",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "french": "fr",
    "german": "de",
    "greek": "el",
    "gujarati": "gu",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "indonesian": "id",
    "italian": "it",
    "japanese": "ja",
    "korean": "ko",
    "malay": "ms",
    "marathi": "mr",
    "nepali": "ne",
    "norwegian": "no",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "romanian": "ro",
    "russian": "ru",
    "spanish": "es",
    "swahili": "sw",
    "swedish": "sv",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "vietnamese": "vi",
}
def normalize_language(lang: Optional[str]) -> Optional[str]:
    """
    Accept either ISO code ('en') or full language name ('english')
    and return ISO code.
    """
    if not lang:
        return None

    lang = lang.strip().lower()

    # If it's a full language name
    if lang in LANGUAGE_NAME_TO_CODE:
        return LANGUAGE_NAME_TO_CODE[lang]

    # Otherwise assume it's already an ISO code
    return lang

# ============= HELPER FUNCTIONS =============

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text from source language to target language
    
    Args:
        text: Text to translate
        source_lang: Source language code (e.g., 'en')
        target_lang: Target language code (e.g., 'es')
    
    Returns:
        Translated text
    """
    try:
        # If source and target are the same, no translation needed
        if source_lang == target_lang:
            return text
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        return translated
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}. Check language codes are valid."
        )


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def generate_audio_filename(text: str, custom_name: Optional[str] = None) -> str:
    """Generate a unique filename for the audio"""
    if custom_name:
        base_name = custom_name.replace(" ", "_")
    else:
        # Create hash of text for unique filename
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"speech_{timestamp}_{text_hash}"
    
    return f"{base_name}.mp3"


def text_to_speech(text: str, output_path: str, language: str = "en"):
    """Convert text to speech and save to file using gTTS"""
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Generate speech using Google TTS
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_path)
    return output_path


# ============= API ENDPOINTS =============

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Text-to-Speech API with Translation",
        "version": "2.0.0",
        "tts_engine": "Google Text-to-Speech (gTTS)",
        "translation_engine": "Google Translate",
        "features": [
            "Text-to-Speech in 100+ languages",
            "Automatic translation between languages",
            "PDF/DOCX/TXT file support",
            "API key authentication"
        ],
        "endpoints": {
            "POST /tts/text": "Convert text to speech (with optional translation)",
            "POST /tts/file": "Upload file and convert to speech (with optional translation)",
            "GET /audio/{filename}": "Download generated audio file",
            "GET /languages": "Get list of supported languages"
        },
        "authentication": "Required - Pass 'X-API-Key' in headers"
    }


@app.get("/languages")
def get_languages():
    """Get list of supported languages"""
    return {
        "supported_languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "hi": "Hindi",
            "ar": "Arabic",
            "nl": "Dutch",
            "pl": "Polish",
            "tr": "Turkish",
            "bn": "Bengali",
            "ta": "Tamil",
            "te": "Telugu",
            "ur": "Urdu",
            "vi": "Vietnamese",
            "th": "Thai",
            "id": "Indonesian",
            "ms": "Malay",
            "fa": "Persian",
            "he": "Hebrew",
            "sw": "Swahili"
        },
        "note": "100+ languages supported for both TTS and translation!",
        "translation_info": {
            "how_to_use": "Set 'translate_from' parameter to enable translation",
            "example": {
                "text": "Hello world",
                "translate_from": "en",
                "language": "es",
                "result": "Audio will say 'Hola mundo' in Spanish"
            }
        }
    }


@app.post("/tts/text", response_model=TTSResponse)
def convert_text_to_speech(
    input_data: TextInput,
    api_key: str = Depends(verify_api_key)
):
    """
    Convert plain text to speech with optional translation
    
    - **text**: The text to convert (required)
    - **language**: Target language code for audio (default: 'en')
    - **translate_from**: Source language code (optional - enables translation)
    - **filename**: Optional custom filename for the audio
    
    Examples:
    
    1. Simple TTS (no translation):
       {"text": "Hello world", "language": "en"}
    
    2. With translation:
       {"text": "Hello world", "translate_from": "en", "language": "es"}
       Result: Spanish audio saying "Hola mundo"
    """
    try:
        original_text = input_data.text
        final_text = original_text
        translation_applied = False

        # Normalize language inputs
        target_language = normalize_language(input_data.language)
        source_language = normalize_language(input_data.translate_from)

        # Apply translation if requested
        if source_language:
            print(f"Translating from {source_language} to {target_language}")
            final_text = translate_text(
                original_text,
                source_language,
                target_language
            )
            translation_applied = True
            print(f"Translation: '{original_text}' → '{final_text}'")

        # Generate filename
        audio_filename = generate_audio_filename(final_text, input_data.filename)
        audio_path = os.path.join(OUTPUT_DIR, audio_filename)

        # Convert text to speech
        text_to_speech(final_text, audio_path, target_language)

        response_message = "Speech generated successfully"
        if translation_applied:
            response_message = (
                f"Text translated from {source_language} "
                f"to {target_language} and speech generated successfully"
            )

        return TTSResponse(
            success=True,
            message=response_message,
            audio_file=audio_filename,
            file_path=f"/audio/{audio_filename}",
            generated_at=datetime.now().isoformat(),
            original_text=original_text if translation_applied else None,
            translated_text=final_text if translation_applied else None,
            translation_applied=translation_applied
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

@app.post("/tts/file", response_model=TTSResponse)
async def convert_file_to_speech(
    file: UploadFile = File(...),
    custom_filename: Optional[str] = None,
    language: str = "en",
    translate_from: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Upload a PDF, DOCX, or TXT file and convert its text to speech
    
    - **file**: PDF, DOCX, or TXT file to process
    - **language**: Target language code for audio (default: 'en')
    - **translate_from**: Source language code (optional - enables translation)
    - **custom_filename**: Optional custom name for output audio
    
    Examples:
    
    1. Extract English PDF and generate English audio:
       file=document.pdf, language="en"
    
    2. Extract English PDF and generate Spanish audio:
       file=document.pdf, translate_from="en", language="es"
    """
    try:
        language = normalize_language(language)
        translate_from = normalize_language(translate_from)
        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract text based on file type
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            text = extract_text_from_pdf(temp_file_path)
        elif file_extension in ['docx', 'doc']:
            text = extract_text_from_docx(temp_file_path)
        elif file_extension == 'txt':
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            os.remove(temp_file_path)
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT")
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in the file")
        
        # Truncate if too long
        if len(text) > 5000:
            text = text[:5000]
            print("Warning: Text truncated to 5000 characters for better TTS performance")
        
        original_text = text
        final_text = text
        translation_applied = False
        
        # Apply translation if requested
        if translate_from:
            print(f"Translating file content from {translate_from} to {language}")
            final_text = translate_text(original_text, translate_from, language)
            translation_applied = True
            print(f"Translation completed: {len(original_text)} → {len(final_text)} characters")
        
        # Generate audio
        audio_filename = generate_audio_filename(final_text, custom_filename)
        audio_path = os.path.join(OUTPUT_DIR, audio_filename)
        
        text_to_speech(final_text, audio_path, language)
        
        response_message = f"Speech generated successfully from {file.filename}"
        if translation_applied:
            response_message = f"File content translated from {translate_from} to {language} and speech generated successfully"
        
        return TTSResponse(
            success=True,
            message=response_message,
            audio_file=audio_filename,
            file_path=f"/audio/{audio_filename}",
            generated_at=datetime.now().isoformat(),
            original_text=original_text[:200] + "..." if translation_applied and len(original_text) > 200 else None,
            translated_text=final_text[:200] + "..." if translation_applied and len(final_text) > 200 else None,
            translation_applied=translation_applied
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/audio/{filename}")
def download_audio(
    filename: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Download a generated audio file
    
    - **filename**: Name of the audio file to download
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


# Health check endpoint
@app.get("/health")
def health_check():
    """Check if the API is running"""
    return {
        "status": "healthy",
        "tts_engine": "gTTS",
        "translation_engine": "Google Translate",
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🎙️  Text-to-Speech API with Translation Starting...")
    print("="*50)
    print(f"📁 Audio files will be saved to: {OUTPUT_DIR}")
    if os.getenv("ENVIRONMENT") != "production":
        print(f"🔑 API Key: {API_KEY}")
    print(f"🌐 TTS Engine: Google Text-to-Speech (gTTS)")
    print(f"🌍 Translation: Google Translate")
    print("="*50 + "\n")
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
