# ⚡ QUICK START CHEATSHEET

## 🚀 Get Started in 3 Commands

```bash
cd tts_api
pip install -r requirements.txt
python main.py
```

---

## 📝 All Important Commands

### Start the API
```bash
python main.py
```

### Run Tests
```bash
python test_api.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### View API Docs (After starting API)
Open browser: `http://localhost:8000/docs`

---

## 🔑 Important Information

**API Key:** `your-secret-api-key-12345`

**API URL:** `http://localhost:8000`

**Generated Files Location:** `generated_audio/`

---

## 🎯 Testing Quick Reference

### Test 1: Simple Text
```bash
curl -X POST "http://localhost:8000/tts/text" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

### Test 2: With Custom Filename
```bash
curl -X POST "http://localhost:8000/tts/text" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing custom name", "filename": "my_audio"}'
```

### Test 3: Upload File
```bash
curl -X POST "http://localhost:8000/tts/file" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -F "file=@sample.txt"
```

### Test 4: Download Audio
```bash
curl -X GET "http://localhost:8000/audio/FILENAME.wav" \
  -H "X-API-Key: your-secret-api-key-12345" \
  --output my_audio.wav
```

### Test 5: Health Check
```bash
curl http://localhost:8000/health
```

---

## 🐍 Python Test Example

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-12345"

# Convert text
response = requests.post(
    f"{API_URL}/tts/text",
    headers={"X-API-Key": API_KEY},
    json={"text": "Hello from Python!"}
)

print(response.json())
```

---

## 📂 Project Files

| File | Purpose |
|------|---------|
| `main.py` | Your API code (the heart) |
| `requirements.txt` | Libraries to install |
| `README.md` | Full documentation |
| `DAY_1_GUIDE.md` | Step-by-step guide |
| `test_api.py` | Automated testing |
| `sample.txt` | Sample file for testing |

---

## 🆘 Emergency Troubleshooting

### API won't start?
```bash
# Try with python3
python3 main.py

# Check if port is free
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

### Dependencies won't install?
```bash
pip install -r requirements.txt --user --upgrade
```

### Test script fails?
```bash
# Make sure API is running first!
# Open new terminal, then run:
python test_api.py
```

---

## 📊 API Endpoints Summary

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/` | ❌ | API info |
| GET | `/health` | ❌ | Health check |
| POST | `/tts/text` | ✅ | Convert text to speech |
| POST | `/tts/file` | ✅ | Convert file to speech |
| GET | `/audio/{filename}` | ✅ | Download audio |

✅ = Requires API key  
❌ = No auth needed

---

## 🎓 What Each HTTP Status Code Means

- **200** - Success! Everything worked
- **401** - Wrong API key (unauthorized)
- **404** - File not found
- **500** - Server error (something broke)

---

## 💡 Pro Tips

1. **Always check if API is running before testing**
2. **Keep the API terminal open - don't close it**
3. **Use the Swagger docs** (`/docs`) - it's the easiest way
4. **Generated audio files stay forever** - delete old ones to save space
5. **First startup is slow** - the AI model downloads once

---

## 📱 Share with Manager

When showing to your manager:

1. Start the API: `python main.py`
2. Open: `http://localhost:8000/docs`
3. Demo the "Try it out" feature
4. Show generated audio files
5. Play one of the audio files

Screenshot these:
- Terminal showing API running ✅
- Swagger docs page ✅
- Successful API response ✅
- Audio file in folder ✅

---

## ⏭️ Next Steps (Day 2)

Tomorrow you'll add:
- SQLite database for tracking
- File metadata storage
- Usage statistics
- Better error messages

---

## 🔗 Useful Links

- FastAPI Docs: https://fastapi.tiangolo.com
- Coqui TTS: https://github.com/coqui-ai/TTS
- Python Requests: https://requests.readthedocs.io

---

## 📞 Need Help?

1. Check `DAY_1_GUIDE.md` for detailed steps
2. Check `ARCHITECTURE_EXPLAINED.md` to understand how it works
3. Check `README.md` for complete documentation
4. Read error messages carefully - they usually tell you what's wrong

---

## ✅ Day 1 Goals

- [x] Install everything
- [x] Run the API
- [x] Make successful API calls
- [x] Generate audio files
- [x] Understand how it works

**Good luck! You've got this! 🚀**
