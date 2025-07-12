#!/usr/bin/env python3
"""
Verification script to check if the Phishing Email Detector is properly set up.
"""

import os
import sys
import importlib
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists."""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (MISSING)")
        return False

def check_python_package(package_name):
    """Check if a Python package is installed."""
    try:
        importlib.import_module(package_name)
        print(f"✅ Python package: {package_name}")
        return True
    except ImportError:
        print(f"❌ Python package: {package_name} (NOT INSTALLED)")
        return False

def check_model_files():
    """Check if model files exist and can be loaded."""
    model_files = [
        'models/phishing_model.pkl',
        'models/feature_extractor.pkl',
        'models/scaler.pkl'
    ]
    
    all_exist = True
    for file_path in model_files:
        if not check_file_exists(file_path, "Model file"):
            all_exist = False
    
    if all_exist:
        try:
            import joblib
            model = joblib.load('models/phishing_model.pkl')
            feature_extractor = joblib.load('models/feature_extractor.pkl')
            scaler = joblib.load('models/scaler.pkl')
            print("✅ Model files can be loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading model files: {e}")
            return False
    
    return False

def check_web_app():
    """Check if the web application can be imported."""
    try:
        from app import app
        print("✅ Flask app can be imported")
        
        # Test basic routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")
            else:
                print(f"❌ Home page returns status code: {response.status_code}")
                return False
            
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint works")
            else:
                print(f"❌ Health endpoint returns status code: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Error with web app: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 Phishing Email Detector Setup Verification")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check core application files
    print("\n📁 Core Application Files:")
    core_files = [
        ('app.py', 'Main Flask application'),
        ('model_trainer.py', 'Model training script'),
        ('feature_extractor.py', 'Feature extraction module'),
        ('data_preprocessor.py', 'Data preprocessing module'),
        ('requirements.txt', 'Python dependencies'),
    ]
    
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check template and static files
    print("\n🎨 Frontend Files:")
    frontend_files = [
        ('templates/index.html', 'Main HTML template'),
        ('static/style.css', 'CSS stylesheet'),
        ('static/script.js', 'JavaScript file'),
    ]
    
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check deployment files
    print("\n🚀 Deployment Files:")
    deployment_files = [
        ('Procfile', 'Heroku process file'),
        ('Dockerfile', 'Docker configuration'),
        ('render.yaml', 'Render deployment config'),
        ('runtime.txt', 'Python runtime specification'),
    ]
    
    for file_path, description in deployment_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check utility files
    print("\n🛠️ Utility Files:")
    utility_files = [
        ('setup.py', 'Setup script'),
        ('test_app.py', 'Test script'),
        ('cli.py', 'Command line interface'),
        ('config.py', 'Configuration file'),
        ('deploy.py', 'Deployment script'),
    ]
    
    for file_path, description in utility_files:
        if not check_file_exists(file_path, description):
            # These are not critical for basic functionality
            pass
    
    # Check directories
    print("\n📂 Directories:")
    directories = [
        ('data', 'Data directory'),
        ('models', 'Models directory'),
        ('static', 'Static files directory'),
        ('templates', 'Templates directory'),
    ]
    
    for dir_path, description in directories:
        if not check_directory_exists(dir_path, description):
            all_checks_passed = False
    
    # Check Python packages
    print("\n🐍 Python Packages:")
    required_packages = [
        'flask', 'pandas', 'numpy', 'sklearn', 'nltk', 
        'beautifulsoup4', 'joblib', 'matplotlib', 'seaborn', 
        'wordcloud', 'gunicorn'
    ]
    
    for package in required_packages:
        if not check_python_package(package):
            all_checks_passed = False
    
    # Check model files
    print("\n🤖 Model Files:")
    if not check_model_files():
        print("⚠️  Model files missing. Run 'python model_trainer.py' to train the model.")
        all_checks_passed = False
    
    # Check web application
    print("\n🌐 Web Application:")
    if not check_web_app():
        all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("🎉 All checks passed! Your Phishing Email Detector is ready to use.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nTo access the web interface:")
        print("  http://localhost:5000")
        print("\nTo use the CLI:")
        print("  python cli.py --help")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nTo set up the application:")
        print("  python setup.py")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nTo train the model:")
        print("  python model_trainer.py")
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
