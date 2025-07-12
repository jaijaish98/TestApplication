"""
Train and save the phishing email detection model.
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from feature_extractor import FeatureExtractor
from data.sample_dataset import create_sample_dataset
import os

class PhishingModelTrainer:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.scaler = StandardScaler()
        self.model = None
        
    def load_data(self):
        """Load or create the dataset."""
        dataset_path = 'data/phishing_dataset.csv'
        
        if not os.path.exists(dataset_path):
            print("Creating sample dataset...")
            dataset = create_sample_dataset()
            dataset.to_csv(dataset_path, index=False)
        else:
            dataset = pd.read_csv(dataset_path)
        
        return dataset
    
    def extract_features(self, emails):
        """Extract features from email texts."""
        print("Extracting features...")
        
        # Fit TF-IDF vectorizer
        self.feature_extractor.fit_tfidf(emails)
        
        # Extract features for all emails
        features = []
        for i, email in enumerate(emails):
            if i % 10 == 0:
                print(f"Processing email {i+1}/{len(emails)}")
            feature_vector = self.feature_extractor.extract_all_features(email)
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_model(self, X, y, model_type='random_forest'):
        """Train the machine learning model."""
        print(f"Training {model_type} model...")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Choose model
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
        else:  # logistic_regression
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000
            )
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)
        
        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Legitimate', 'Phishing'],
                   yticklabels=['Legitimate', 'Phishing'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('static/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return accuracy, y_test, y_pred, y_pred_proba
    
    def save_model(self):
        """Save the trained model and components."""
        print("Saving model...")
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save model components
        joblib.dump(self.model, 'models/phishing_model.pkl')
        joblib.dump(self.feature_extractor, 'models/feature_extractor.pkl')
        joblib.dump(self.scaler, 'models/scaler.pkl')
        
        print("Model saved successfully!")
    
    def train_and_save(self, model_type='random_forest'):
        """Complete training pipeline."""
        # Load data
        dataset = self.load_data()
        print(f"Loaded dataset with {len(dataset)} samples")
        
        # Extract features
        X = self.extract_features(dataset['email_text'].tolist())
        y = dataset['label'].values
        
        print(f"Feature matrix shape: {X.shape}")
        
        # Train model
        accuracy, y_test, y_pred, y_pred_proba = self.train_model(X, y, model_type)
        
        # Save model
        self.save_model()
        
        return accuracy

def main():
    """Main training function."""
    trainer = PhishingModelTrainer()
    
    # Train Random Forest model
    print("Training Random Forest model...")
    rf_accuracy = trainer.train_and_save('random_forest')
    
    print(f"\nTraining completed!")
    print(f"Random Forest Accuracy: {rf_accuracy:.4f}")

if __name__ == "__main__":
    main()
