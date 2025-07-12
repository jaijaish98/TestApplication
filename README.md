# Phishing Email Detector 🛡️

An AI-powered web application that detects phishing emails using Natural Language Processing (NLP) and machine learning techniques.

## 🚀 Features

- **Real-time Analysis**: Instant phishing detection for email content
- **Advanced NLP**: Sophisticated text preprocessing and feature extraction
- **Machine Learning**: Random Forest classifier with high accuracy
- **Interactive UI**: Clean, responsive web interface built with Bootstrap
- **Visual Analytics**: Word clouds and confidence score visualization
- **REST API**: JSON API endpoints for integration
- **Containerized**: Docker support for easy deployment
- **Cloud Ready**: Configured for Heroku, Render, and other platforms

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask
- **Machine Learning**: Scikit-learn, NLTK
- **Data Processing**: Pandas, NumPy, BeautifulSoup
- **Visualization**: Matplotlib, Seaborn, WordCloud
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment**: Docker, Gunicorn, Heroku/Render

## 📁 Project Structure

```
phishing-email-detector/
├── app.py                 # Main Flask application
├── model_trainer.py       # ML model training script
├── feature_extractor.py   # Feature extraction utilities
├── data_preprocessor.py   # Text preprocessing functions
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── Procfile              # Heroku deployment config
├── render.yaml           # Render deployment config
├── runtime.txt           # Python version specification
├── data/
│   └── sample_dataset.py # Sample dataset generator
├── models/               # Trained model storage
├── static/
│   ├── style.css        # Custom CSS styles
│   └── script.js        # Frontend JavaScript
└── templates/
    └── index.html       # Main web interface
```

## 🔧 Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaijaish98/TestApplication.git
   cd TestApplication
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model**
   ```bash
   python model_trainer.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t phishing-detector .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 phishing-detector
   ```

## 🌐 Deployment

### Heroku

1. **Install Heroku CLI**
2. **Login and create app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### Render

1. **Connect your GitHub repository**
2. **Use the provided `render.yaml` configuration**
3. **Deploy automatically on push**

### Hugging Face Spaces

1. **Create a new Space**
2. **Upload your files**
3. **Set runtime to Python**

## 📊 Model Performance

The machine learning model uses the following features:
- Text length and word count
- Number of URLs and email addresses
- Suspicious word frequency
- TF-IDF vector representation
- Linguistic patterns (uppercase ratio, punctuation)

**Performance Metrics:**
- Accuracy: ~95%+
- Precision: High for both classes
- Recall: Balanced detection
- F1-Score: Optimized for real-world usage

## 🔍 API Endpoints

### POST /predict
Analyze email content for phishing detection.

**Request:**
```json
{
  "email_text": "Your email content here..."
}
```

**Response:**
```json
{
  "prediction": "Phishing",
  "confidence_phishing": 0.85,
  "confidence_legitimate": 0.15,
  "is_phishing": true,
  "wordcloud": "base64_encoded_image"
}
```

### GET /health
Health check endpoint.

### GET /api/info
API information and documentation.

## 🧪 Testing

Test the application with sample emails:

**Phishing Example:**
```
URGENT: Your account will be suspended! Click here immediately to verify your information and avoid account closure. Act now before it's too late!
```

**Legitimate Example:**
```
Thank you for your recent purchase. Your order #12345 has been shipped and will arrive within 3-5 business days.
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Always verify suspicious emails through official channels and never share sensitive information based solely on automated analysis.

## 🔗 Links

- **Live Demo**: [Your deployed app URL]
- **Documentation**: [API docs URL]
- **Issues**: [GitHub Issues URL]

## 👨‍💻 Author

**Jai Jaish**
- GitHub: [@jaijaish98](https://github.com/jaijaish98)
- Email: jaijaish98@gmail.com

---

Made with ❤️ and AI