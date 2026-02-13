# 🎙️ Text-to-Speech API

A simple REST API that converts text to speech using open-source AI models.

## Features

✅ Convert plain text to speech  
✅ Upload PDF, DOCX, or TXT files for conversion  
✅ API key authentication  
✅ Store generated audio files  
✅ Download generated speech files  

## Day 1 Setup Guide

### Step 1: Install Python (if not already installed)

Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Install Dependencies

Navigate to the project folder and install requirements:
```bash
pip install -r requirements.txt
```

**Note:** First installation will take 5-10 minutes as it downloads the TTS model.

### Step 3: Run the API

```bash
python main.py
```

The API will start on `http://localhost:8000`

You should see:
```
🎙️  Text-to-Speech API Starting...
📁 Audio files will be saved to: generated_audio
🔑 API Key: your-secret-api-key-12345
```

## Testing the API

### Option 1: Using the Browser

1. Open your browser and go to: `http://localhost:8000/docs`
2. You'll see an interactive API documentation (Swagger UI)
3. Click on any endpoint to test it

### Option 2: Using cURL (Command Line)

**Test 1: Convert plain text to speech**
```bash
curl -X POST "http://localhost:8000/tts/text" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test of the text to speech API."}'
```

**Test 2: Upload a text file**
```bash
curl -X POST "http://localhost:8000/tts/file" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -F "file=@sample.txt"
```

**Test 3: Download generated audio**
```bash
curl -X GET "http://localhost:8000/audio/speech_20240101_120000_abc123.wav" \
  -H "X-API-Key: your-secret-api-key-12345" \
  --output speech.wav
```

### Option 3: Using Python

```python
import requests

# API configuration
API_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-12345"
headers = {"X-API-Key": API_KEY}

# Convert text to speech
response = requests.post(
    f"{API_URL}/tts/text",
    headers=headers,
    json={"text": "Hello, this is a test!"}
)

print(response.json())
# Output: {'success': True, 'audio_file': 'speech_xxx.wav', ...}

# Download the audio file
audio_file = response.json()['audio_file']
audio_response = requests.get(
    f"{API_URL}/audio/{audio_file}",
    headers=headers
)

with open("output.wav", "wb") as f:
    f.write(audio_response.content)

print("Audio saved to output.wav")
```

## API Endpoints

### 1. Root Endpoint
- **URL:** `GET /`
- **Auth:** Not required
- **Description:** Get API information

### 2. Convert Text to Speech
- **URL:** `POST /tts/text`
- **Auth:** Required (X-API-Key header)
- **Body:**
  ```json
  {
    "text": "Your text here",
    "filename": "optional_custom_name"
  }
  ```

### 3. Convert File to Speech
- **URL:** `POST /tts/file`
- **Auth:** Required (X-API-Key header)
- **Form Data:**
  - `file`: PDF, DOCX, or TXT file
  - `custom_filename`: (optional) custom name for output

### 4. Download Audio
- **URL:** `GET /audio/{filename}`
- **Auth:** Required (X-API-Key header)

### 5. Health Check
- **URL:** `GET /health`
- **Auth:** Not required
- **Description:** Check if API is running

## Authentication

All protected endpoints require an API key in the header:
```
X-API-Key: your-secret-api-key-12345
```

**⚠️ IMPORTANT:** Change the API key in `main.py` before deploying!

## File Storage

Generated audio files are stored in the `generated_audio/` directory with timestamps and unique identifiers.

## Troubleshooting

### Problem: "TTS model loading failed"
**Solution:** First run takes time to download the model. Wait 5-10 minutes.

### Problem: "Port 8000 already in use"
**Solution:** Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

### Problem: "No module named 'xxx'"
**Solution:** Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

## Day 1 Checklist

- [ ] Install Python and dependencies
- [ ] Run the API successfully
- [ ] Test with browser (http://localhost:8000/docs)
- [ ] Send a text conversion request
- [ ] Download the generated audio file
- [ ] Test with a PDF or TXT file

## What's Next?

**Day 2:** Add database for tracking files, improve storage  
**Day 3:** Add error handling, deploy, write final documentation

## Project Structure

```
tts_api/
├── main.py              # Main API code
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── generated_audio/    # Created automatically
│   └── speech_*.wav    # Generated audio files
└── test_sample.txt     # Sample file for testing
```

## Notes

- Current TTS model: Tacotron2-DDC (fast, good quality)
- Audio format: WAV (uncompressed)
- Text limit: 5000 characters per request (for performance)

## Support

If you get stuck, check:
1. Is Python installed? (`python --version`)
2. Are dependencies installed? (`pip list | grep fastapi`)
3. Is the API running? (check the terminal)
4. Is the API key correct in your requests?
