"""
Test script for Phishing Email Detector
"""

import unittest
import json
import os
import sys
import joblib
from app import app

class TestPhishingDetector(unittest.TestCase):
    
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample test emails
        self.phishing_email = """
        URGENT: Your account will be suspended! Click here immediately to verify 
        your information and avoid account closure. Act now before it's too late!
        """
        
        self.legitimate_email = """
        Thank you for your recent purchase. Your order #12345 has been shipped 
        and will arrive within 3-5 business days.
        """
    
    def test_home_page(self):
        """Test home page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phishing Email Detector', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_api_info_endpoint(self):
        """Test API info endpoint."""
        response = self.app.get('/api/info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertIn('version', data)
    
    def test_predict_phishing_email(self):
        """Test prediction for phishing email."""
        response = self.app.post('/predict',
                                data=json.dumps({'email_text': self.phishing_email}),
                                content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('prediction', data)
            self.assertIn('confidence_phishing', data)
            self.assertIn('confidence_legitimate', data)
            self.assertIn('is_phishing', data)
        else:
            print(f"Prediction failed: {response.data}")
    
    def test_predict_legitimate_email(self):
        """Test prediction for legitimate email."""
        response = self.app.post('/predict',
                                data=json.dumps({'email_text': self.legitimate_email}),
                                content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('prediction', data)
            self.assertIn('confidence_phishing', data)
            self.assertIn('confidence_legitimate', data)
            self.assertIn('is_phishing', data)
        else:
            print(f"Prediction failed: {response.data}")
    
    def test_predict_empty_email(self):
        """Test prediction with empty email."""
        response = self.app.post('/predict',
                                data=json.dumps({'email_text': ''}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_predict_invalid_json(self):
        """Test prediction with invalid JSON."""
        response = self.app.post('/predict',
                                data='invalid json',
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

class TestModelComponents(unittest.TestCase):
    
    def test_model_files_exist(self):
        """Test that model files exist."""
        model_files = [
            'models/phishing_model.pkl',
            'models/feature_extractor.pkl',
            'models/scaler.pkl'
        ]
        
        for file_path in model_files:
            self.assertTrue(os.path.exists(file_path), f"Model file {file_path} does not exist")
    
    def test_model_loading(self):
        """Test that models can be loaded."""
        try:
            model = joblib.load('models/phishing_model.pkl')
            feature_extractor = joblib.load('models/feature_extractor.pkl')
            scaler = joblib.load('models/scaler.pkl')
            
            self.assertIsNotNone(model)
            self.assertIsNotNone(feature_extractor)
            self.assertIsNotNone(scaler)
            
        except Exception as e:
            self.fail(f"Failed to load model components: {e}")

class TestFeatureExtraction(unittest.TestCase):
    
    def setUp(self):
        """Set up feature extractor."""
        try:
            from feature_extractor import FeatureExtractor
            self.feature_extractor = FeatureExtractor()
        except ImportError as e:
            self.skipTest(f"Could not import FeatureExtractor: {e}")
    
    def test_basic_features(self):
        """Test basic feature extraction."""
        email_text = "This is a test email with some content."
        features = self.feature_extractor.extract_basic_features(email_text)
        
        self.assertIsInstance(features, type(features))
        self.assertGreater(len(features), 0)
    
    def test_empty_email_features(self):
        """Test feature extraction with empty email."""
        features = self.feature_extractor.extract_basic_features("")
        self.assertIsInstance(features, type(features))

class TestDataPreprocessing(unittest.TestCase):
    
    def setUp(self):
        """Set up preprocessor."""
        try:
            from data_preprocessor import EmailPreprocessor
            self.preprocessor = EmailPreprocessor()
        except ImportError as e:
            self.skipTest(f"Could not import EmailPreprocessor: {e}")
    
    def test_html_removal(self):
        """Test HTML tag removal."""
        html_text = "<p>This is <b>bold</b> text</p>"
        clean_text = self.preprocessor.remove_html_tags(html_text)
        
        self.assertNotIn('<', clean_text)
        self.assertNotIn('>', clean_text)
    
    def test_url_extraction(self):
        """Test URL extraction."""
        text_with_url = "Visit https://example.com for more info"
        urls = self.preprocessor.extract_urls(text_with_url)
        
        self.assertGreater(len(urls), 0)
        self.assertIn('https://example.com', urls)
    
    def test_email_preprocessing(self):
        """Test complete email preprocessing."""
        email_text = "<p>URGENT: Click https://phishing.com NOW!</p>"
        processed = self.preprocessor.preprocess_email(email_text)
        
        self.assertIsInstance(processed, str)

def run_tests():
    """Run all tests."""
    print("🧪 Running Phishing Email Detector Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestPhishingDetector,
        TestModelComponents,
        TestFeatureExtraction,
        TestDataPreprocessing
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
