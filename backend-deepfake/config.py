import os

class Config:
    SECRET_KEY = 'dev-secret-key-for-local-testing'
    
    UPLOAD_FOLDER = 'uploads'
    MODEL_PATH = 'audio_classification_model.h5'
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    ALLOWED_EXTENSIONS = {'wav'}
    
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    DETECTION_THRESHOLD = 0.15

