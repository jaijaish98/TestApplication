#!/usr/bin/env python3
"""
Command Line Interface for Phishing Email Detector
"""

import argparse
import sys
import os
import joblib
from pathlib import Path

def load_model_components():
    """Load trained model components."""
    try:
        model = joblib.load('models/phishing_model.pkl')
        feature_extractor = joblib.load('models/feature_extractor.pkl')
        scaler = joblib.load('models/scaler.pkl')
        return model, feature_extractor, scaler
    except FileNotFoundError as e:
        print(f"❌ Model files not found: {e}")
        print("Please train the model first: python model_trainer.py")
        return None, None, None

def predict_email(email_text, model, feature_extractor, scaler):
    """Predict if email is phishing."""
    try:
        # Extract features
        features = feature_extractor.extract_all_features(email_text)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        return {
            'prediction': 'Phishing' if prediction == 1 else 'Legitimate',
            'confidence_phishing': float(probability[1]),
            'confidence_legitimate': float(probability[0]),
            'is_phishing': bool(prediction == 1)
        }
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

def analyze_file(file_path, model, feature_extractor, scaler):
    """Analyze email from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            email_text = f.read()
        
        result = predict_email(email_text, model, feature_extractor, scaler)
        if result:
            print(f"\n📧 Analysis Results for: {file_path}")
            print("=" * 50)
            print(f"Prediction: {result['prediction']}")
            print(f"Phishing Confidence: {result['confidence_phishing']:.2%}")
            print(f"Legitimate Confidence: {result['confidence_legitimate']:.2%}")
            
            if result['is_phishing']:
                print("⚠️  WARNING: This email appears to be PHISHING!")
            else:
                print("✅ This email appears to be LEGITIMATE")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def interactive_mode(model, feature_extractor, scaler):
    """Interactive mode for email analysis."""
    print("\n🛡️ Interactive Phishing Email Detector")
    print("=" * 50)
    print("Enter email content (press Ctrl+D or Ctrl+Z when finished):")
    print("Type 'quit' to exit")
    
    while True:
        try:
            print("\n📧 Enter email content:")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip().lower() == 'quit':
                        return
                    lines.append(line)
                except EOFError:
                    break
            
            email_text = '\n'.join(lines)
            if not email_text.strip():
                print("❌ No content entered. Please try again.")
                continue
            
            result = predict_email(email_text, model, feature_extractor, scaler)
            if result:
                print("\n📊 Analysis Results:")
                print("=" * 30)
                print(f"Prediction: {result['prediction']}")
                print(f"Phishing Confidence: {result['confidence_phishing']:.2%}")
                print(f"Legitimate Confidence: {result['confidence_legitimate']:.2%}")
                
                if result['is_phishing']:
                    print("⚠️  WARNING: This email appears to be PHISHING!")
                else:
                    print("✅ This email appears to be LEGITIMATE")
            
            print("\nPress Enter to analyze another email or type 'quit' to exit...")
            if input().strip().lower() == 'quit':
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

def batch_analyze(directory, model, feature_extractor, scaler):
    """Analyze all text files in a directory."""
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    text_files = list(directory_path.glob('*.txt')) + list(directory_path.glob('*.eml'))
    
    if not text_files:
        print(f"❌ No text files found in: {directory}")
        return
    
    print(f"\n📁 Batch Analysis: {len(text_files)} files found")
    print("=" * 50)
    
    results = []
    for file_path in text_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                email_text = f.read()
            
            result = predict_email(email_text, model, feature_extractor, scaler)
            if result:
                results.append({
                    'file': file_path.name,
                    'prediction': result['prediction'],
                    'confidence': result['confidence_phishing'] if result['is_phishing'] else result['confidence_legitimate'],
                    'is_phishing': result['is_phishing']
                })
                
                status = "⚠️ PHISHING" if result['is_phishing'] else "✅ LEGITIMATE"
                confidence = result['confidence_phishing'] if result['is_phishing'] else result['confidence_legitimate']
                print(f"{file_path.name:<30} {status:<15} ({confidence:.1%})")
        
        except Exception as e:
            print(f"{file_path.name:<30} ❌ ERROR: {e}")
    
    # Summary
    if results:
        phishing_count = sum(1 for r in results if r['is_phishing'])
        legitimate_count = len(results) - phishing_count
        
        print("\n📊 Summary:")
        print(f"Total files analyzed: {len(results)}")
        print(f"Phishing emails: {phishing_count}")
        print(f"Legitimate emails: {legitimate_count}")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Phishing Email Detector CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py -i                    # Interactive mode
  python cli.py -f email.txt          # Analyze single file
  python cli.py -d emails/            # Batch analyze directory
  python cli.py -t "Click here now!"  # Analyze text directly
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interactive', action='store_true',
                      help='Interactive mode')
    group.add_argument('-f', '--file', type=str,
                      help='Analyze email from file')
    group.add_argument('-d', '--directory', type=str,
                      help='Batch analyze all text files in directory')
    group.add_argument('-t', '--text', type=str,
                      help='Analyze email text directly')
    
    args = parser.parse_args()
    
    print("🛡️ Phishing Email Detector CLI")
    print("=" * 50)
    
    # Load model components
    print("Loading model components...")
    model, feature_extractor, scaler = load_model_components()
    
    if not all([model, feature_extractor, scaler]):
        sys.exit(1)
    
    print("✅ Model loaded successfully!")
    
    # Execute based on arguments
    if args.interactive:
        interactive_mode(model, feature_extractor, scaler)
    elif args.file:
        analyze_file(args.file, model, feature_extractor, scaler)
    elif args.directory:
        batch_analyze(args.directory, model, feature_extractor, scaler)
    elif args.text:
        result = predict_email(args.text, model, feature_extractor, scaler)
        if result:
            print(f"\n📧 Analysis Results:")
            print("=" * 30)
            print(f"Prediction: {result['prediction']}")
            print(f"Phishing Confidence: {result['confidence_phishing']:.2%}")
            print(f"Legitimate Confidence: {result['confidence_legitimate']:.2%}")
            
            if result['is_phishing']:
                print("⚠️  WARNING: This email appears to be PHISHING!")
            else:
                print("✅ This email appears to be LEGITIMATE")

if __name__ == "__main__":
    main()
