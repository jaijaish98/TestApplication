"""
Configuration settings for Phishing Email Detector
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = FLASK_ENV == 'development'
    
    # Application settings
    APP_NAME = 'Phishing Email Detector'
    APP_VERSION = '1.0.0'
    
    # Model settings
    MODEL_DIR = BASE_DIR / 'models'
    DATA_DIR = BASE_DIR / 'data'
    STATIC_DIR = BASE_DIR / 'static'
    
    # Model file paths
    MODEL_PATH = MODEL_DIR / 'phishing_model.pkl'
    FEATURE_EXTRACTOR_PATH = MODEL_DIR / 'feature_extractor.pkl'
    SCALER_PATH = MODEL_DIR / 'scaler.pkl'
    
    # Dataset settings
    DATASET_PATH = DATA_DIR / 'phishing_dataset.csv'
    
    # ML settings
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    CV_FOLDS = 5
    
    # Feature extraction settings
    MAX_FEATURES = 1000
    NGRAM_RANGE = (1, 2)
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Security settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # API settings
    API_RATE_LIMIT = '100 per hour'
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'testing'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
