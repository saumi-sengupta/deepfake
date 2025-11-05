from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from logging.handlers import RotatingFileHandler
from model_utils import DeepfakeDetector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Deepfake Detection API startup')

detector = DeepfakeDetector(app.config['MODEL_PATH'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector.model is not None
    }), 200

@app.route('/api/detect', methods=['POST'])
def detect_deepfake():
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'success': False
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'success': False
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Only WAV files are allowed',
                'success': False
            }), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        app.logger.info(f'Processing file: {filename}')

        result = detector.predict(filepath)

        os.remove(filepath)

        if result['success']:
            app.logger.info(f'Prediction successful: {result["prediction"]} (confidence: {result["confidence"]:.4f})')
            return jsonify({
                'success': True,
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'is_deepfake': result['is_deepfake'],
                'filename': filename
            }), 200
        else:
            app.logger.error(f'Prediction failed: {result["error"]}')
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500

    except Exception as e:
        app.logger.error(f'Unexpected error: {str(e)}')
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'error': 'File too large. Maximum size is 16MB',
        'success': False
    }), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

