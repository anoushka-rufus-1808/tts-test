"""
Test script for Text-to-Speech API
Run this after starting the API to verify everything works
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-12345"

def test_api():
    """Run all API tests"""
    
    print("="*60)
    print("🧪 Testing Text-to-Speech API")
    print("="*60)
    
    headers = {"X-API-Key": API_KEY}
    
    # Test 1: Check API is running
    print("\n✅ Test 1: Checking API health...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print(f"   Success! API is running: {response.json()}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: Cannot connect to API. Is it running?")
        print(f"   Error details: {e}")
        return
    
    # Test 2: Convert text to speech
    print("\n✅ Test 2: Converting text to speech...")
    try:
        data = {
            "text": "Hello! This is to test whether text to speech works. If you can hear this, then it works perfectly well.",
            "filename": "test_speech"
        }
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success! Audio generated:")
            print(f"   - File: {result['audio_file']}")
            print(f"   - Path: {result['file_path']}")
            print(f"   - Time: {result['generated_at']}")
            audio_filename = result['audio_file']
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Download the audio
    print("\n✅ Test 3: Downloading generated audio...")
    try:
        response = requests.get(
            f"{API_URL}/audio/{audio_filename}",
            headers=headers
        )
        
        if response.status_code == 200:
            output_file = "test_output.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"   Success! Audio saved to: {output_file}")
            print(f"   File size: {len(response.content)} bytes")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 4: Test authentication
    print("\n✅ Test 4: Testing authentication...")
    try:
        # Test with wrong API key
        bad_headers = {"X-API-Key": "wrong-key"}
        response = requests.post(
            f"{API_URL}/tts/text",
            headers=bad_headers,
            json={"text": "test"}
        )
        
        if response.status_code == 401:
            print("   Success! Authentication is working (rejected bad key)")
        else:
            print(f"   ⚠️  Warning: Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print("\n📝 Next steps:")
    print("   1. Check generated_audio/ folder for your audio files")
    print("   2. Play test_output.wav to hear the speech")
    print("   3. Try the API docs at: http://localhost:8000/docs")
    print("   4. Test with your own text or files")
    print("\n")

if __name__ == "__main__":
    test_api()
