# Deepfake Audio Detection Backend

Flask API for detecting deepfake audio using CNN + BiLSTM model.

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your Model

Place your trained model file in the root directory:
```
audio_classification_model.h5
```

### 3. Run the Server

```bash
python app.py
```

Server will start at: `http://localhost:5000`

## Test the API

### Option 1: Use the Web Interface

Open `index.html` in your browser and upload a WAV file.

### Option 2: Use Python Script

```bash
python test_api.py path/to/audio.wav
```

### Option 3: Use cURL

```bash
curl -X POST http://localhost:5000/api/detect -F "file=@audio.wav"
```

## API Endpoints

**Health Check:**
```
GET /api/health
```

**Detect Deepfake:**
```
POST /api/detect
```
Upload WAV file (max 16MB, 16kHz sample rate)

**Response:**
```json
{
  "success": true,
  "prediction": "FAKE",
  "confidence": 0.9160,
  "is_deepfake": true,
  "filename": "audio.wav"
}
```

## Project Structure

```
backend-deepfake/
├── app.py                          Flask application
├── model_utils.py                  Model prediction logic
├── feature_extraction.py           MFCC feature extraction
├── config.py                       Configuration
├── requirements.txt                Dependencies
├── index.html                      Sample frontend
├── test_api.py                     Test script
├── audio_classification_model.h5   Your trained model
└── model_norm.ipynb                Original training notebook
```

## Troubleshooting

**Model not found:**
- Make sure `audio_classification_model.h5` is in the root directory

**Import errors:**
- Run: `pip install -r requirements.txt`

**Port already in use:**
- Change PORT in `.env` file or kill the process using port 5000

**Frontend can't connect:**
- Make sure Flask server is running
- Check the API_URL in `index.html` matches your server address

