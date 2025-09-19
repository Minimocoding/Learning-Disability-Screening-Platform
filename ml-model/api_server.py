from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Add the models directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from ld_classifier import LearningDifferenceClassifier

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global model instance
classifier = None

def initialize_model():
    """Initialize or load the ML model."""
    global classifier
    classifier = LearningDifferenceClassifier()
    
    model_path = 'models/ld_classifier.joblib'
    
    if os.path.exists(model_path):
        print("Loading pre-trained model...")
        try:
            classifier.load_model(model_path)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("Training new model...")
            train_new_model()
    else:
        print("No pre-trained model found. Training new model...")
        train_new_model()

def train_new_model():
    """Train and save a new model."""
    global classifier
    try:
        classifier.train()
        os.makedirs('models', exist_ok=True)
        classifier.save_model('models/ld_classifier.joblib')
        print("✅ New model trained and saved!")
    except Exception as e:
        print(f"❌ Error training model: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': classifier is not None and classifier.is_trained,
        'version': '1.0.0'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict learning differences based on questionnaire responses.
    
    Expected input:
    {
        "answers": [0, 1, 2, 1, 0, ...] // Array of 50 integers (0-2)
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        if 'answers' not in data:
            return jsonify({'error': 'Missing "answers" field'}), 400
        
        answers = data['answers']
        
        # Validate answers
        if not isinstance(answers, list):
            return jsonify({'error': 'Answers must be a list'}), 400
        
        if len(answers) != 50:
            return jsonify({'error': 'Must provide exactly 50 answers'}), 400
        
        if not all(isinstance(x, int) and 0 <= x <= 2 for x in answers):
            return jsonify({'error': 'All answers must be integers between 0 and 2'}), 400
        
        # Check if model is available
        if not classifier or not classifier.is_trained:
            return jsonify({'error': 'ML model not available'}), 503
        
        # Make prediction
        result = classifier.predict(answers)
        
        # Add metadata
        result['modelVersion'] = 'v1.0-sklearn'
        result['timestamp'] = pd.Timestamp.now().isoformat()
        
        return jsonify({
            'success': True,
            'prediction': result
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            'error': 'Internal server error during prediction',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/retrain', methods=['POST'])
def retrain_model():
    """
    Retrain the model with new data (admin endpoint).
    """
    try:
        # In a real application, you'd authenticate this endpoint
        # and accept new training data in the request
        
        print("Retraining model...")
        train_new_model()
        
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully'
        })
        
    except Exception as e:
        print(f"Retraining error: {e}")
        return jsonify({
            'error': 'Failed to retrain model',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the current model."""
    try:
        if not classifier or not classifier.is_trained:
            return jsonify({
                'loaded': False,
                'error': 'No model loaded'
            })
        
        return jsonify({
            'loaded': True,
            'version': 'v1.0-sklearn',
            'features': {
                'ld_detection': True,
                'type_classification': classifier.type_classifier is not None,
                'mental_health_screening': True
            },
            'supported_types': ['dyslexia', 'dyscalculia', 'dysgraphia']
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get model info',
            'details': str(e) if app.debug else None
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🧠 Initializing Learning Helper ML API...")
    
    # Initialize the model
    initialize_model()
    
    # Get configuration
    port = int(os.getenv('ML_API_PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting ML API server on port {port}")
    print(f"📊 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)