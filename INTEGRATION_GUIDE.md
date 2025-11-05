# Frontend-Backend Integration Guide

## Setup Instructions

### 1. Start the Backend (Flask API)

```bash
# Navigate to backend directory
cd backend-deepfake

# Activate virtual environment (if not already activated)
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend should start on `http://localhost:5000`

### 2. Start the Frontend (React)

Open a new terminal:

```bash
# Navigate to frontend directory
cd deepfake-ui

# Install dependencies (if not already installed)
npm install

# Start the React development server
npm start
```

The frontend should start on `http://localhost:3000`

## How It Works

1. **User uploads a .wav file** through the React frontend
2. **Frontend sends the file** to the Flask backend via POST request to `/api/detect`
3. **Backend processes the audio** using the trained deepfake detection model
4. **Backend returns prediction** with:
   - `prediction`: "REAL" or "FAKE"
   - `confidence`: Confidence score (0-1)
   - `is_deepfake`: Boolean value
5. **Frontend displays the verdict** with the confidence score

## API Endpoints

### Health Check
```
GET http://localhost:5000/api/health
```

### Deepfake Detection
```
POST http://localhost:5000/api/detect
Content-Type: multipart/form-data

Body:
- file: .wav audio file
```

Response:
```json
{
  "success": true,
  "prediction": "REAL",
  "confidence": 0.05,
  "is_deepfake": false,
  "filename": "example.wav"
}
```

## Testing

1. Ensure the backend is running (check `http://localhost:5000/api/health`)
2. Open the frontend at `http://localhost:3000`
3. Upload a .wav file
4. Watch the analyzing animation
5. See the verdict with confidence score

## Troubleshooting

### CORS Issues
- Make sure Flask-CORS is installed: `pip install flask-cors==4.0.0`
- Backend already has CORS enabled for all origins

### Connection Refused
- Verify the Flask server is running on port 5000
- Check that the API_BASE_URL in `App.jsx` matches your backend URL

### File Upload Errors
- Only .wav files are accepted
- Maximum file size is 16MB
- Convert your audio files to .wav format before uploading

### Model Errors
- Ensure `audio_classification_model.h5` exists in the backend directory
- Check that TensorFlow is properly installed

