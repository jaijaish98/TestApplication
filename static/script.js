// JavaScript for Phishing Email Detector

document.addEventListener('DOMContentLoaded', function() {
    const emailForm = document.getElementById('emailForm');
    const emailText = document.getElementById('emailText');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

    // Form submission handler
    emailForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeEmail();
    });

    // Sample email buttons (if you want to add them later)
    function loadSampleEmail(type) {
        const samples = {
            phishing: "URGENT: Your account will be suspended! Click here immediately to verify your information and avoid account closure. Act now before it's too late!",
            legitimate: "Thank you for your recent purchase. Your order #12345 has been shipped and will arrive within 3-5 business days."
        };
        
        emailText.value = samples[type];
        emailText.focus();
    }

    // Clear form function
    window.clearForm = function() {
        emailText.value = '';
        resultsSection.style.display = 'none';
        emailText.focus();
    };

    // Analyze email function
    async function analyzeEmail() {
        const text = emailText.value.trim();
        
        if (!text) {
            showAlert('Please enter email content to analyze.', 'warning');
            return;
        }

        // Show loading modal
        loadingModal.show();
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email_text: text
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred');
            }

            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            showAlert('Error analyzing email: ' + error.message, 'danger');
        } finally {
            loadingModal.hide();
            analyzeBtn.disabled = false;
        }
    }

    // Display results function
    function displayResults(data) {
        const predictionResult = document.getElementById('predictionResult');
        const legitimateBar = document.getElementById('legitimateBar');
        const phishingBar = document.getElementById('phishingBar');
        const legitimateScore = document.getElementById('legitimateScore');
        const phishingScore = document.getElementById('phishingScore');
        const wordcloudImage = document.getElementById('wordcloudImage');

        // Create result display
        const isPhishing = data.is_phishing;
        const confidence = isPhishing ? data.confidence_phishing : data.confidence_legitimate;
        
        predictionResult.innerHTML = `
            <div class="${isPhishing ? 'result-phishing' : 'result-legitimate'} fade-in">
                <div class="result-icon">
                    <i class="fas ${isPhishing ? 'fa-exclamation-triangle' : 'fa-shield-alt'}"></i>
                </div>
                <div class="result-title">${data.prediction}</div>
                <div class="result-subtitle">
                    Confidence: ${(confidence * 100).toFixed(1)}%
                </div>
            </div>
        `;

        // Update progress bars
        const legitimatePercent = (data.confidence_legitimate * 100).toFixed(1);
        const phishingPercent = (data.confidence_phishing * 100).toFixed(1);

        legitimateBar.style.width = legitimatePercent + '%';
        phishingBar.style.width = phishingPercent + '%';
        
        legitimateScore.textContent = legitimatePercent + '%';
        phishingScore.textContent = phishingPercent + '%';

        // Display word cloud if available
        if (data.wordcloud) {
            wordcloudImage.innerHTML = `
                <img src="data:image/png;base64,${data.wordcloud}" 
                     alt="Word Cloud" 
                     class="img-fluid fade-in">
            `;
        } else {
            wordcloudImage.innerHTML = '<p class="text-muted">Word cloud not available</p>';
        }

        // Show results section with animation
        resultsSection.style.display = 'block';
        resultsSection.classList.add('fade-in');
        
        // Scroll to results
        resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    // Show alert function
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert alert at the top of the main container
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Add sample email buttons dynamically (optional)
    function addSampleButtons() {
        const formCard = document.querySelector('.card-body');
        const sampleButtonsDiv = document.createElement('div');
        sampleButtonsDiv.className = 'mb-3';
        sampleButtonsDiv.innerHTML = `
            <label class="form-label">Try sample emails:</label>
            <div class="btn-group w-100" role="group">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="loadSampleEmail('phishing')">
                    <i class="fas fa-exclamation-triangle me-1"></i>
                    Phishing Sample
                </button>
                <button type="button" class="btn btn-outline-success btn-sm" onclick="loadSampleEmail('legitimate')">
                    <i class="fas fa-check me-1"></i>
                    Legitimate Sample
                </button>
            </div>
        `;
        
        // Insert before the textarea
        const textareaDiv = formCard.querySelector('.mb-3');
        formCard.insertBefore(sampleButtonsDiv, textareaDiv);
    }

    // Make loadSampleEmail globally available
    window.loadSampleEmail = loadSampleEmail;

    // Add sample buttons
    addSampleButtons();

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to analyze
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            analyzeEmail();
        }
        
        // Ctrl+L to clear
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            clearForm();
        }
    });

    // Add tooltip for keyboard shortcuts
    analyzeBtn.setAttribute('title', 'Click to analyze or press Ctrl+Enter');
    
    // Character counter for textarea
    function addCharacterCounter() {
        const counterDiv = document.createElement('div');
        counterDiv.className = 'text-muted small mt-1';
        counterDiv.id = 'charCounter';
        
        emailText.parentNode.appendChild(counterDiv);
        
        function updateCounter() {
            const count = emailText.value.length;
            counterDiv.textContent = `${count} characters`;
            
            if (count > 5000) {
                counterDiv.className = 'text-warning small mt-1';
            } else {
                counterDiv.className = 'text-muted small mt-1';
            }
        }
        
        emailText.addEventListener('input', updateCounter);
        updateCounter();
    }
    
    addCharacterCounter();

    // Auto-resize textarea
    function autoResize() {
        emailText.style.height = 'auto';
        emailText.style.height = emailText.scrollHeight + 'px';
    }
    
    emailText.addEventListener('input', autoResize);
    
    // Focus on textarea when page loads
    emailText.focus();
});
