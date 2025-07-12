"""
Setup script for Phishing Email Detector
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("Creating directories...")
    directories = ["models", "data", "static/images"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def train_model():
    """Train the machine learning model."""
    print("Training the model...")
    try:
        subprocess.check_call([sys.executable, "model_trainer.py"])
        print("✅ Model trained successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error training model: {e}")
        return False

def check_model_files():
    """Check if model files exist."""
    model_files = [
        "models/phishing_model.pkl",
        "models/feature_extractor.pkl",
        "models/scaler.pkl"
    ]
    
    missing_files = []
    for file_path in model_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing model files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All model files present!")
        return True

def run_tests():
    """Run basic tests."""
    print("Running basic tests...")
    
    try:
        # Test imports
        import pandas as pd
        import numpy as np
        import sklearn
        import nltk
        import flask
        print("✅ All required packages imported successfully!")
        
        # Test model loading
        if check_model_files():
            import joblib
            model = joblib.load('models/phishing_model.pkl')
            feature_extractor = joblib.load('models/feature_extractor.pkl')
            scaler = joblib.load('models/scaler.pkl')
            print("✅ Model files loaded successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Phishing Email Detector...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation.")
        return False
    
    # Train model if not exists
    if not check_model_files():
        print("Model files not found. Training new model...")
        if not train_model():
            print("❌ Setup failed at model training.")
            return False
    else:
        print("✅ Model files already exist!")
    
    # Run tests
    if not run_tests():
        print("❌ Setup failed at testing.")
        return False
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nTo access the web interface:")
    print("  http://localhost:5000")
    
    return True

if __name__ == "__main__":
    main()
