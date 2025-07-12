"""
Feature extraction utilities for phishing email detection.
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from data_preprocessor import EmailPreprocessor

class FeatureExtractor:
    def __init__(self):
        self.preprocessor = EmailPreprocessor()
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.suspicious_words = [
            'urgent', 'immediate', 'act now', 'limited time', 'expires',
            'click here', 'click now', 'verify', 'confirm', 'update',
            'suspend', 'suspended', 'account', 'security', 'alert',
            'warning', 'congratulations', 'winner', 'prize', 'lottery',
            'free', 'bonus', 'offer', 'deal', 'discount', 'save',
            'money', 'cash', 'credit', 'loan', 'debt', 'investment',
            'guarantee', 'risk-free', 'no obligation', 'act fast',
            'don\'t delay', 'hurry', 'rush', 'now', 'today only',
            'limited offer', 'exclusive', 'special', 'amazing',
            'incredible', 'unbelievable', 'fantastic', 'wonderful'
        ]
        
    def extract_basic_features(self, email_text):
        """Extract basic statistical features from email text."""
        if not email_text:
            return np.zeros(8)
        
        # Text length
        text_length = len(email_text)
        
        # Word count
        word_count = len(email_text.split())
        
        # Character count
        char_count = len(email_text)
        
        # Number of URLs
        urls = self.preprocessor.extract_urls(email_text)
        url_count = len(urls)
        
        # Number of email addresses
        emails = self.preprocessor.extract_emails(email_text)
        email_count = len(emails)
        
        # Number of suspicious words
        suspicious_count = sum(1 for word in self.suspicious_words 
                             if word.lower() in email_text.lower())
        
        # Ratio of uppercase letters
        uppercase_ratio = sum(1 for c in email_text if c.isupper()) / max(len(email_text), 1)
        
        # Number of exclamation marks
        exclamation_count = email_text.count('!')
        
        return np.array([
            text_length, word_count, char_count, url_count,
            email_count, suspicious_count, uppercase_ratio, exclamation_count
        ])
    
    def extract_advanced_features(self, email_text):
        """Extract advanced linguistic features."""
        if not email_text:
            return np.zeros(5)
        
        # Average word length
        words = email_text.split()
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        
        # Number of sentences
        sentence_count = len(re.split(r'[.!?]+', email_text))
        
        # Average sentence length
        avg_sentence_length = len(words) / max(sentence_count, 1)
        
        # Number of question marks
        question_count = email_text.count('?')
        
        # Number of capital letters
        capital_count = sum(1 for c in email_text if c.isupper())
        
        return np.array([
            avg_word_length, sentence_count, avg_sentence_length,
            question_count, capital_count
        ])
    
    def fit_tfidf(self, email_texts):
        """Fit TF-IDF vectorizer on training data."""
        processed_texts = [self.preprocessor.preprocess_email(text) for text in email_texts]
        self.tfidf_vectorizer.fit(processed_texts)
        
    def extract_tfidf_features(self, email_text):
        """Extract TF-IDF features from email text."""
        processed_text = self.preprocessor.preprocess_email(email_text)
        tfidf_features = self.tfidf_vectorizer.transform([processed_text])
        return tfidf_features.toarray()[0]
    
    def extract_all_features(self, email_text):
        """Extract all features from email text."""
        basic_features = self.extract_basic_features(email_text)
        advanced_features = self.extract_advanced_features(email_text)
        tfidf_features = self.extract_tfidf_features(email_text)
        
        # Combine all features
        all_features = np.concatenate([basic_features, advanced_features, tfidf_features])
        return all_features
    
    def get_feature_names(self):
        """Get names of all features."""
        basic_names = [
            'text_length', 'word_count', 'char_count', 'url_count',
            'email_count', 'suspicious_count', 'uppercase_ratio', 'exclamation_count'
        ]
        advanced_names = [
            'avg_word_length', 'sentence_count', 'avg_sentence_length',
            'question_count', 'capital_count'
        ]
        tfidf_names = [f'tfidf_{i}' for i in range(len(self.tfidf_vectorizer.get_feature_names_out()))]
        
        return basic_names + advanced_names + tfidf_names
