# Quick Start Guide - Deepfake Audio Detection

## 🚀 Starting Your Application

### Step 1: Start Backend Server

Open a terminal and run:

```bash
cd backend-deepfake
python app.py
```

✅ You should see:
```
* Running on http://0.0.0.0:5000
* Deepfake Detection API startup
```

### Step 2: Test Backend (Optional)

In another terminal:

```bash
cd backend-deepfake
python test_api.py 128-Tum.wav
```

### Step 3: Start Frontend

Open a new terminal and run:

```bash
cd deepfake-ui
npm start
```

✅ Browser should automatically open to `http://localhost:3000`

## 🎯 Testing the Application

1. **Upload a .wav file** by clicking the upload button or dragging & dropping
2. **Watch the animation** as your file is analyzed
3. **View the verdict** with confidence score:
   - **Green "Real"** = Authentic audio
   - **Red "Fake"** = AI-generated/Deepfake audio

## 📝 Test Files

The backend includes test audio files you can use:
- `backend-deepfake/128-Tum.wav`
- `backend-deepfake/pianos-by-jtwayne-7-174717.wav`
- `backend-deepfake/sunflower-street-drumloop-85bpm-163900.wav`

## 🔧 What Changed

### Frontend (`deepfake-ui/src/App.jsx`)
- ✅ Added API integration with Flask backend
- ✅ Real file upload to `/api/detect` endpoint
- ✅ Display actual prediction results
- ✅ Show confidence score
- ✅ Error handling for connection issues

### Backend (`backend-deepfake/app.py`)
- ✅ Already configured with CORS
- ✅ Ready to accept .wav files
- ✅ Returns prediction with confidence score

## 🎨 Features

- **Real-time Processing**: Upload → Analyze → Results
- **Beautiful UI**: Smooth animations and transitions
- **Confidence Score**: See how confident the model is
- **Error Handling**: Clear error messages if something goes wrong
- **File Validation**: Only accepts .wav files

## 🐛 Troubleshooting

### "Failed to connect to backend"
- Make sure Flask is running on port 5000
- Check terminal for error messages

### "Please upload a .wav file"
- Convert your audio to .wav format first
- Use tools like Audacity, FFmpeg, or online converters

### Model not loading
- Verify `audio_classification_model.h5` exists in `backend-deepfake/`
- Check Python dependencies are installed

## 📊 Understanding Results

The model returns a confidence score between 0 and 1:
- **Low score (< 0.15)**: Likely REAL audio
- **High score (> 0.15)**: Likely FAKE/Deepfake audio

The threshold is set to 0.15 (configurable in `config.py`)

---

**Ready to detect deepfakes! 🎙️🔍**

