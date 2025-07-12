"""
Generate sample phishing dataset for training the model.
"""

import pandas as pd
import numpy as np

def create_sample_dataset():
    """Create a sample dataset with phishing and legitimate emails."""
    
    # Sample phishing emails
    phishing_emails = [
        "URGENT: Your account will be suspended! Click here immediately to verify your information and avoid account closure. Act now before it's too late!",
        "Congratulations! You've won $1,000,000 in our lottery! Click this link to claim your prize now. Limited time offer!",
        "SECURITY ALERT: Suspicious activity detected on your account. Verify your identity immediately by clicking here or your account will be locked.",
        "Your PayPal account has been limited. Please update your information by clicking the link below to restore full access.",
        "FINAL NOTICE: Your subscription will expire today. Click here to renew and save 50% off. Don't miss this amazing deal!",
        "Your bank account has been compromised. Click here immediately to secure your account and prevent unauthorized access.",
        "You have received a money transfer of $5,000. Click here to accept the transfer and provide your banking details.",
        "URGENT: IRS Tax Refund of $2,847 is pending. Click here to claim your refund before the deadline expires.",
        "Your credit score has dropped significantly. Click here for a free credit report and repair services. Act now!",
        "WINNER! You've been selected for a special investment opportunity. Guaranteed returns of 300%. Click here to invest now!",
        "Your Amazon account has been hacked. Click here immediately to change your password and secure your account.",
        "ALERT: Your computer is infected with viruses. Download our antivirus software now to protect your data.",
        "You qualify for a $50,000 loan with no credit check. Click here to apply now and get instant approval.",
        "Your Netflix subscription has expired. Click here to renew and continue watching your favorite shows.",
        "URGENT: Your email account will be deleted. Click here to verify your account and prevent deletion.",
        "You've inherited $2.5 million from a distant relative. Click here to claim your inheritance now.",
        "Your iPhone has been selected for a free upgrade. Click here to claim your new iPhone 15 Pro Max.",
        "SECURITY WARNING: Your password has been compromised. Click here to reset your password immediately.",
        "You've won a free vacation to Hawaii! Click here to claim your all-expenses-paid trip. Limited time only!",
        "Your Google account has been accessed from an unknown device. Click here to secure your account now."
    ]
    
    # Sample legitimate emails
    legitimate_emails = [
        "Thank you for your recent purchase. Your order #12345 has been shipped and will arrive within 3-5 business days.",
        "Your monthly statement is now available. You can view it by logging into your account on our website.",
        "We're excited to announce our new product line. Visit our store to see the latest additions to our collection.",
        "Your appointment with Dr. Smith has been confirmed for tomorrow at 2:00 PM. Please arrive 15 minutes early.",
        "The team meeting scheduled for Friday has been moved to Monday at 10:00 AM. Please update your calendar.",
        "Your subscription renewal is coming up next month. We'll send you a reminder closer to the renewal date.",
        "Thank you for attending our webinar. The recording and slides are now available in your account.",
        "Your flight booking has been confirmed. Please check in online 24 hours before your departure.",
        "We've received your support ticket and will respond within 24 hours. Thank you for your patience.",
        "Your order has been delivered successfully. We hope you enjoy your purchase and thank you for choosing us.",
        "The software update you requested has been completed. Please restart your application to see the changes.",
        "Your annual report is ready for download. You can access it from your dashboard at any time.",
        "We're hosting a customer appreciation event next month. We'd love to have you join us for an evening of networking.",
        "Your project milestone has been approved. You can proceed to the next phase as planned.",
        "The conference you registered for has been rescheduled to next month. We'll send updated details soon.",
        "Your feedback on our recent service has been received. We appreciate your input and will use it to improve.",
        "The training session you enrolled in will begin next week. Please review the pre-course materials.",
        "Your warranty registration has been processed successfully. Keep this email for your records.",
        "We're conducting a customer satisfaction survey. Your participation would help us serve you better.",
        "Your account settings have been updated as requested. The changes will take effect within 24 hours."
    ]
    
    # Create DataFrame
    data = []
    
    # Add phishing emails
    for email in phishing_emails:
        data.append({'email_text': email, 'label': 1})  # 1 for phishing
    
    # Add legitimate emails
    for email in legitimate_emails:
        data.append({'email_text': email, 'label': 0})  # 0 for legitimate
    
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Create and save the dataset
    dataset = create_sample_dataset()
    dataset.to_csv('data/phishing_dataset.csv', index=False)
    print(f"Dataset created with {len(dataset)} samples")
    print(f"Phishing emails: {sum(dataset['label'])}")
    print(f"Legitimate emails: {len(dataset) - sum(dataset['label'])}")
