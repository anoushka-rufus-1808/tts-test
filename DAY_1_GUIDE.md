# 📅 DAY 1 COMPLETE GUIDE

## Your Mission Today
Build a working Text-to-Speech API and test it successfully.

---

## STEP-BY-STEP INSTRUCTIONS

### ⚙️ STEP 1: Install Python (5 minutes)

**Check if you have Python:**
```bash
python --version
```
or
```bash
python3 --version
```

**You need Python 3.8 or higher.** If not installed:
- Windows: Download from https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

---

### 📦 STEP 2: Install Dependencies (10 minutes)

Open terminal/command prompt in the `tts_api` folder:

```bash
cd tts_api
pip install -r requirements.txt
```

**⏰ This will take 5-10 minutes** because it downloads:
- FastAPI (web framework)
- TTS model (AI for speech generation)
- PDF/DOC readers

**If you get permission errors**, try:
```bash
pip install -r requirements.txt --user
```

---

### 🚀 STEP 3: Start the API (2 minutes)

```bash
python main.py
```

You should see:
```
🎙️  Text-to-Speech API Starting...
📁 Audio files will be saved to: generated_audio
🔑 API Key: your-secret-api-key-12345
INFO: Started server process
INFO: Uvicorn running on http://0.0.0.0:8000
```

**✅ SUCCESS!** Your API is running!

**⚠️ Don't close this terminal** - keep it running while you test.

---

### 🧪 STEP 4: Test the API (15 minutes)

Open a **NEW terminal window** (keep the first one running).

#### Method 1: Interactive Documentation (EASIEST)

1. Open your browser
2. Go to: `http://localhost:8000/docs`
3. You'll see a beautiful interactive API page
4. Click on `POST /tts/text`
5. Click "Try it out"
6. Enter:
   - X-API-Key: `your-secret-api-key-12345`
   - Request body:
     ```json
     {
       "text": "Hello, this is my first test!"
     }
     ```
7. Click "Execute"
8. You should get a success response!

#### Method 2: Python Test Script (RECOMMENDED)

```bash
python test_api.py
```

This will automatically test everything and save a `test_output.wav` file.

#### Method 3: Manual cURL

```bash
curl -X POST "http://localhost:8000/tts/text" \
  -H "X-API-Key: your-secret-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing the API from command line"}'
```

---

### 🎵 STEP 5: Listen to Your Audio (5 minutes)

1. Open the `generated_audio` folder in your project
2. Find the `.wav` file that was created
3. Double-click to play it
4. You should hear your text spoken!

---

### 📄 STEP 6: Test with a File (5 minutes)

Using the browser docs (`http://localhost:8000/docs`):

1. Click on `POST /tts/file`
2. Click "Try it out"
3. Enter API Key: `your-secret-api-key-12345`
4. Click "Choose File" and select `sample.txt`
5. Click "Execute"
6. Check the `generated_audio` folder for the new audio file

---

## ✅ DAY 1 CHECKLIST

By end of day, you should have:

- [x] Python installed and working
- [x] All dependencies installed
- [x] API running successfully
- [x] Tested text-to-speech conversion
- [x] Generated and listened to audio files
- [x] Tested file upload (PDF/TXT)
- [x] Understood how authentication works

---

## 🐛 TROUBLESHOOTING

### Problem: "python: command not found"
**Solution:** Try `python3` instead of `python`

### Problem: "pip: command not found"
**Solution:** Try `pip3` instead of `pip`

### Problem: "Address already in use"
**Solution:** Another program is using port 8000. Change in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to 8001
```

### Problem: "ModuleNotFoundError"
**Solution:** Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

### Problem: TTS model loading takes forever
**Solution:** First time takes 5-10 minutes. Be patient. It's downloading the AI model.

### Problem: "API Key invalid"
**Solution:** Make sure you're using: `your-secret-api-key-12345` exactly

---

## 📚 WHAT YOU LEARNED TODAY

1. **APIs**: How to build REST APIs with FastAPI
2. **Authentication**: How API keys protect endpoints
3. **TTS**: How text-to-speech AI works
4. **File handling**: Reading PDFs, DOC files in Python
5. **File storage**: Saving and serving generated files

---

## 🎯 PREPARE FOR DAY 2

Tomorrow you'll add:
- Database to track all generated files
- Better file organization
- Usage statistics
- More error handling

### Quick Prep (5 minutes):

1. Read about SQLite (simple database)
2. Think about what data you want to track:
   - When was audio generated?
   - What was the original text?
   - File size?
   - User who created it?

---

## 📸 TAKE A SCREENSHOT

For your intern manager, take screenshots of:
1. The API running in terminal
2. The Swagger docs page (http://localhost:8000/docs)
3. A successful API response
4. The `generated_audio` folder with files

---

## 🎉 CONGRATULATIONS!

You built a working AI-powered API in one day! 

**Day 1 Status: ✅ COMPLETE**

Tomorrow you'll make it even better with proper data storage and tracking.

---

## QUICK REFERENCE

**Start API:**
```bash
python main.py
```

**Test API:**
```bash
python test_api.py
```

**View Docs:**
```
http://localhost:8000/docs
```

**API Key:**
```
your-secret-api-key-12345
```

**Endpoints:**
- `POST /tts/text` - Convert text
- `POST /tts/file` - Convert file
- `GET /audio/{filename}` - Download audio
- `GET /health` - Check status
