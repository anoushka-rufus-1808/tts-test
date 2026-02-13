# 🏗️ API ARCHITECTURE EXPLAINED

## How Your API Works (Simple Explanation)

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│  (You, or anyone making requests to the API)                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ 1. Sends request with text/file + API key
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI SERVER                            │
│                   (main.py running)                          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 1: Authentication Check                        │   │
│  │  - Verifies API key is correct                       │   │
│  │  - If wrong, returns 401 error                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          │ 2. API key is valid              │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 2: Process Input                               │   │
│  │  - If text: use directly                             │   │
│  │  - If PDF: extract text from PDF                     │   │
│  │  - If DOCX: extract text from Word doc               │   │
│  │  - If TXT: read the text file                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          │ 3. Text ready                    │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 3: Text-to-Speech (TTS)                        │   │
│  │  - Sends text to Coqui TTS model                     │   │
│  │  - AI generates speech audio                         │   │
│  │  - Saves as .wav file                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          │ 4. Audio generated               │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Step 4: Store & Respond                             │   │
│  │  - Saves audio to generated_audio/ folder            │   │
│  │  - Returns JSON with file info                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ 5. Returns response
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│  Receives JSON response with:                                │
│  - audio_file: "speech_20240101_120000.wav"                  │
│  - file_path: "/audio/speech_20240101_120000.wav"            │
│  - success: true                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Code Structure (Simplified)

```python
# 1. IMPORTS - Get all the tools we need
from fastapi import FastAPI  # Web framework
from TTS.api import TTS      # Text-to-speech AI

# 2. SETUP - Initialize everything
app = FastAPI()              # Create the API
tts = TTS(model_name="...")  # Load the AI model
API_KEY = "your-key"         # Set the password

# 3. AUTHENTICATION - Check who's allowed
def verify_api_key(key):
    if key != API_KEY:
        return "Not allowed!"
    return "Welcome!"

# 4. ENDPOINTS - Define what the API can do

@app.post("/tts/text")       # Endpoint for text input
def convert_text(text):
    # Check authentication
    # Convert text to speech
    # Save the audio file
    # Return success message
    
@app.post("/tts/file")       # Endpoint for file input
def convert_file(file):
    # Check authentication
    # Extract text from file
    # Convert to speech
    # Save the audio file
    # Return success message

@app.get("/audio/{filename}") # Endpoint to download audio
def download_audio(filename):
    # Check authentication
    # Find the file
    # Send it to user
```

---

## Key Concepts Explained

### 1. **FastAPI**
Think of it like a restaurant:
- API = Restaurant
- Endpoints = Menu items
- Requests = Customer orders
- Responses = Food delivered

### 2. **Authentication**
Like a VIP club:
- API Key = VIP card
- Without the right card, you can't get in
- Every request must show the card

### 3. **TTS Model**
Like a robot voice actor:
- You give it a script (text)
- It reads it out loud
- Records it as audio
- Saves the recording

### 4. **File Storage**
Like a filing cabinet:
- Each audio gets a unique name
- Stored in the `generated_audio/` folder
- Can be retrieved anytime using the filename

---

## Request/Response Flow Example

### Example 1: Text to Speech

**Request:**
```json
POST /tts/text
Headers: X-API-Key: your-secret-api-key-12345
Body: {
  "text": "Hello world"
}
```

**What happens:**
1. API receives request ✅
2. Checks API key ✅
3. Takes "Hello world" text
4. Sends to TTS model
5. TTS generates speech
6. Saves as `speech_20240101_120000_abc123.wav`
7. Returns response

**Response:**
```json
{
  "success": true,
  "message": "Speech generated successfully",
  "audio_file": "speech_20240101_120000_abc123.wav",
  "file_path": "/audio/speech_20240101_120000_abc123.wav",
  "generated_at": "2024-01-01T12:00:00"
}
```

### Example 2: File Upload

**Request:**
```
POST /tts/file
Headers: X-API-Key: your-secret-api-key-12345
Form Data: file=document.pdf
```

**What happens:**
1. API receives PDF file ✅
2. Checks API key ✅
3. Saves PDF temporarily
4. Extracts text from PDF: "This is the content..."
5. Sends text to TTS model
6. TTS generates speech
7. Deletes temporary PDF
8. Saves audio as `.wav`
9. Returns response

---

## Folder Structure After Running

```
tts_api/
├── main.py                    # Your API code
├── requirements.txt           # Libraries needed
├── README.md                  # Documentation
├── DAY_1_GUIDE.md            # This guide
├── test_api.py               # Test script
├── sample.txt                # Sample file for testing
│
├── generated_audio/          # Created automatically
│   ├── speech_20240101_120000_abc123.wav
│   ├── speech_20240101_120530_def456.wav
│   └── test_speech.wav
│
└── __pycache__/              # Python cache (ignore this)
```

---

## Common Questions

**Q: Why FastAPI and not Flask?**
A: FastAPI is faster, has automatic documentation, and better type checking.

**Q: Why Coqui TTS?**
A: It's free, open-source, works offline, and produces good quality speech.

**Q: Can I use a different AI model?**
A: Yes! In Day 2-3, we can switch to other models if needed.

**Q: Is the API key secure?**
A: For learning, yes. For production, you'd use OAuth2 or JWT tokens.

**Q: How many requests can it handle?**
A: Depends on your computer. Usually 10-50 concurrent requests.

**Q: Can I deploy this online?**
A: Yes! Day 3 will cover deployment options.

---

## Technical Terms You Should Know

| Term | Simple Explanation | Example |
|------|-------------------|---------|
| **API** | A way for programs to talk to each other | Like a waiter taking your order |
| **Endpoint** | A specific URL that does one thing | `/tts/text` converts text |
| **HTTP Method** | Type of request (GET, POST, etc.) | POST = send data, GET = retrieve data |
| **Headers** | Extra info sent with request | API key goes here |
| **Request Body** | The main data you're sending | The text to convert |
| **Response** | What the API sends back | Success message + file info |
| **Status Code** | Number showing if request worked | 200 = success, 401 = not authorized |
| **JSON** | Way to structure data | `{"key": "value"}` |

---

## Why This Architecture?

1. **Separation of Concerns**: Each function does ONE thing
2. **Easy to Test**: Can test each part separately
3. **Easy to Extend**: Add new features without breaking old ones
4. **Secure**: Authentication protects your API
5. **Scalable**: Can handle more users by adding servers

---

## What You'll Add Tomorrow (Day 2)

```
Current:
User → API → TTS → Save File → Done

Day 2:
User → API → TTS → Save File → Database Entry → Done
                                ↓
                         Track: who, when, what, size
```

You'll add a database to remember:
- Who created each audio?
- When was it created?
- How big is the file?
- What was the original text?

This makes it a COMPLETE production-ready API! 🚀
