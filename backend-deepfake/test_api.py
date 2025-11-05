import requests
import sys

def test_health():
    url = "http://localhost:5000/api/health"
    try:
        response = requests.get(url)
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_detection(audio_file_path):
    url = "http://localhost:5000/api/detect"
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        print(f"Detection Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if result.get('success'):
            print(f"\nResult: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Is Deepfake: {result['is_deepfake']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Deepfake Detection API")
    print("="*50)
    
    if test_health():
        print("✓ API is running\n")
    else:
        print("✗ API is not running")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"Testing with: {audio_file}")
        print("="*50)
        test_detection(audio_file)
    else:
        print("Usage: python test_api.py <audio.wav>")

