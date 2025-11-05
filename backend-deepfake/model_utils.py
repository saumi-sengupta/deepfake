import tensorflow as tf
import numpy as np
from feature_extraction import extract_features
import os

class DeepfakeDetector:
    def __init__(self, model_path, threshold=0.15):
        self.model = None
        self.threshold = threshold
        self.load_model(model_path)
    
    def load_model(self, model_path):
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            self.model = tf.keras.models.load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def predict(self, audio_file_path):
        try:
            features = extract_features(audio_file_path, max_pad_len=200)
            
            if features is None:
                return {
                    'success': False,
                    'error': 'Failed to extract features from audio file'
                }
            
            features = np.expand_dims(features, axis=-1)
            features = np.expand_dims(features, axis=0)
            
            prediction = self.model.predict(features, verbose=0)
            confidence_score = float(prediction[0][0])
            
            is_deepfake = confidence_score > self.threshold
            prediction_label = "FAKE" if is_deepfake else "REAL"
            
            return {
                'success': True,
                'prediction': prediction_label,
                'confidence': confidence_score,
                'is_deepfake': is_deepfake
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction error: {str(e)}'
            }

