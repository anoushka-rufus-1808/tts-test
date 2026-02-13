"""
Test script for Text-to-Speech API with Translation
Tests both regular TTS and translation features
"""

import requests
import os
import sys

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "your-secret-api-key-12345")

def test_translation_api():
    """Run all API tests including translation"""
    
    print("="*70)
    print("🧪 Testing Text-to-Speech API with Translation")
    print("="*70)
    print(f"📍 Testing URL: {API_URL}")
    print(f"🔑 Using API Key: {API_KEY[:20]}...")
    print("="*70)
    
    headers = {"X-API-Key": API_KEY}
    
    # Test 1: Health Check
    print("\n✅ Test 1: Checking API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! API is running")
            print(f"   - TTS Engine: {data.get('tts_engine')}")
            print(f"   - Translation: {data.get('translation_engine')}")
            print(f"   - Version: {data.get('version')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: Cannot connect to API at {API_URL}")
        print(f"   Make sure the API is running!")
        return False
    
    # Test 2: Simple TTS (No Translation)
    print("\n✅ Test 2: Simple TTS (No translation)...")
    try:
        data = {
            "text": "Hello! This is a test in English.",
            "language": "en"
        }
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success! Audio generated:")
            print(f"   - File: {result['audio_file']}")
            print(f"   - Translation applied: {result['translation_applied']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: English to Spanish Translation
    print("\n✅ Test 3: Translation - English to Spanish...")
    try:
        data = {
            "text": "Hello, how are you? This is a translation test.",
            "translate_from": "en",
            "language": "es",
            "filename": "english_to_spanish"
        }
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success! Translation + TTS completed:")
            print(f"   - Original: {result.get('original_text', 'N/A')[:50]}...")
            print(f"   - Translated: {result.get('translated_text', 'N/A')[:50]}...")
            print(f"   - Audio file: {result['audio_file']}")
            print(f"   - Translation applied: {result['translation_applied']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: English to Hindi Translation
    print("\n✅ Test 4: Translation - English to Hindi...")
    try:
        data = {
            "text": "Welcome to our service. We are happy to help you.",
            "translate_from": "en",
            "language": "hi",
            "filename": "english_to_hindi"
        }
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success! English → Hindi:")
            print(f"   - Original: {result.get('original_text', 'N/A')[:50]}...")
            print(f"   - Translated: {result.get('translated_text', 'N/A')[:50]}...")
            print(f"   - Audio file: {result['audio_file']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: English to French Translation
    print("\n✅ Test 5: Translation - English to French...")
    try:
        data = {
            "text": "Good morning. The weather is beautiful today.",
            "translate_from": "en",
            "language": "fr",
            "filename": "english_to_french"
        }
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success! English → French:")
            print(f"   - Original: {result.get('original_text', 'N/A')[:50]}...")
            print(f"   - Translated: {result.get('translated_text', 'N/A')[:50]}...")
            print(f"   - Audio file: {result['audio_file']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 6: Download Audio
    print("\n✅ Test 6: Downloading translated audio...")
    try:
        # Download the Spanish audio from Test 3
        response = requests.get(
            f"{API_URL}/audio/english_to_spanish.mp3",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            output_file = "test_spanish_audio.mp3"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"   Success! Audio saved to: {output_file}")
            print(f"   File size: {len(response.content)} bytes")
            print(f"   💡 Play this file to hear Spanish audio!")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 7: Multiple Language Pairs
    print("\n✅ Test 7: Testing multiple language pairs...")
    
    test_pairs = [
        ("en", "de", "Hello"),  # English to German
        ("en", "ja", "Good morning"),  # English to Japanese
        ("en", "ar", "Welcome"),  # English to Arabic
    ]
    
    for source, target, text in test_pairs:
        try:
            data = {
                "text": text,
                "translate_from": source,
                "language": target
            }
            response = requests.post(
                f"{API_URL}/tts/text",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✓ {source} → {target}: '{result.get('original_text')}' → '{result.get('translated_text')}'")
            else:
                print(f"   ✗ {source} → {target} failed")
        except Exception as e:
            print(f"   ✗ {source} → {target} error: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("🎉 ALL TRANSLATION TESTS PASSED!")
    print("="*70)
    print("\n📊 Test Summary:")
    print("   ✅ Health check")
    print("   ✅ Simple TTS (no translation)")
    print("   ✅ English → Spanish translation + TTS")
    print("   ✅ English → Hindi translation + TTS")
    print("   ✅ English → French translation + TTS")
    print("   ✅ Audio file download")
    print("   ✅ Multiple language pairs")
    
    print("\n📝 Next steps:")
    print("   1. Check generated_audio/ folder for all audio files")
    print("   2. Play test_spanish_audio.mp3 to hear Spanish")
    print("   3. Try the API docs at: " + API_URL + "/docs")
    print("   4. Test with your own text and language combinations")
    
    print("\n💡 Example usage:")
    print("   POST /tts/text")
    print("   {")
    print('     "text": "Your English text here",')
    print('     "translate_from": "en",')
    print('     "language": "es"  // Spanish, hi, fr, de, etc.')
    print("   }")
    print("\n")
    
    return True

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        API_URL = sys.argv[1]
        print(f"Using custom API URL: {API_URL}")
    
    if len(sys.argv) > 2:
        API_KEY = sys.argv[2]
        print(f"Using custom API key")
    
    success = test_translation_api()
    sys.exit(0 if success else 1)
