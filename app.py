"""
Flask web application for phishing email detection.
"""

import os
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json

app = Flask(__name__)

# Global variables for model components
model = None
feature_extractor = None
scaler = None

def load_model_components():
    """Load the trained model and components."""
    global model, feature_extractor, scaler
    
    try:
        model = joblib.load('models/phishing_model.pkl')
        feature_extractor = joblib.load('models/feature_extractor.pkl')
        scaler = joblib.load('models/scaler.pkl')
        print("Model components loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model components: {e}")
        return False

def predict_phishing(email_text):
    """Predict if an email is phishing or legitimate."""
    if not all([model, feature_extractor, scaler]):
        return None, None, "Model not loaded"
    
    try:
        # Extract features
        features = feature_extractor.extract_all_features(email_text)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        # Get confidence scores
        confidence_legitimate = probability[0]
        confidence_phishing = probability[1]
        
        result = {
            'prediction': 'Phishing' if prediction == 1 else 'Legitimate',
            'confidence_phishing': float(confidence_phishing),
            'confidence_legitimate': float(confidence_legitimate),
            'is_phishing': bool(prediction == 1)
        }
        
        return result, None
        
    except Exception as e:
        return None, f"Error during prediction: {str(e)}"

def generate_wordcloud(text, title="Word Cloud"):
    """Generate word cloud from text."""
    try:
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(text)
        
        # Create plot
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold')
        
        # Save to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for email prediction."""
    try:
        data = request.get_json()
        email_text = data.get('email_text', '').strip()
        
        if not email_text:
            return jsonify({'error': 'Email text is required'}), 400
        
        # Make prediction
        result, error = predict_phishing(email_text)
        
        if error:
            return jsonify({'error': error}), 500
        
        # Generate word cloud
        wordcloud_image = generate_wordcloud(email_text, "Email Content Word Cloud")
        
        response = {
            'prediction': result['prediction'],
            'confidence_phishing': result['confidence_phishing'],
            'confidence_legitimate': result['confidence_legitimate'],
            'is_phishing': result['is_phishing'],
            'wordcloud': wordcloud_image
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    model_status = "loaded" if all([model, feature_extractor, scaler]) else "not loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status
    })

@app.route('/api/info')
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Phishing Email Detector API',
        'version': '1.0.0',
        'description': 'AI-powered phishing email detection using NLP and machine learning',
        'endpoints': {
            '/': 'Main web interface',
            '/predict': 'POST - Predict if email is phishing',
            '/health': 'GET - Health check',
            '/api/info': 'GET - API information'
        }
    })

def initialize_app():
    """Initialize the application."""
    print("Initializing Phishing Email Detector...")
    
    # Load model components
    if not load_model_components():
        print("Warning: Model components not found. Please train the model first.")
        print("Run: python model_trainer.py")
    
    print("Application initialized successfully!")

if __name__ == '__main__':
    initialize_app()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
