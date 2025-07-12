"""
Data preprocessing utilities for phishing email detection.
"""

import re
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class EmailPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
    def remove_html_tags(self, text):
        """Remove HTML tags from text."""
        if not text:
            return ""
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    
    def remove_urls(self, text):
        """Remove URLs from text."""
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.sub('', text)
    
    def remove_emails(self, text):
        """Remove email addresses from text."""
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        return email_pattern.sub('', text)
    
    def remove_special_chars(self, text):
        """Remove special characters and digits."""
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def tokenize_and_clean(self, text):
        """Tokenize text and remove stopwords."""
        if not text:
            return []
        
        # Tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and short words
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Stem words
        tokens = [self.stemmer.stem(token) for token in tokens]
        
        return tokens
    
    def preprocess_email(self, email_text):
        """Complete preprocessing pipeline for email text."""
        if not email_text:
            return ""
        
        # Remove HTML tags
        text = self.remove_html_tags(email_text)
        
        # Remove URLs and emails
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        
        # Remove special characters
        text = self.remove_special_chars(text)
        
        # Tokenize and clean
        tokens = self.tokenize_and_clean(text)
        
        # Join tokens back to string
        return ' '.join(tokens)
    
    def extract_urls(self, text):
        """Extract URLs from text."""
        if not text:
            return []
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.findall(text)
    
    def extract_emails(self, text):
        """Extract email addresses from text."""
        if not text:
            return []
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        return email_pattern.findall(text)
