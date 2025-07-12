"""
Deployment script for Phishing Email Detector
"""

import os
import subprocess
import sys
import argparse

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    # Check if required files exist
    required_files = [
        'requirements.txt',
        'app.py',
        'model_trainer.py',
        'Procfile'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files present!")
    return True

def setup_local():
    """Set up local development environment."""
    print("🚀 Setting up local development environment...")
    
    if not check_prerequisites():
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    # Train model
    if not run_command("python model_trainer.py", "Training model"):
        return False
    
    # Run tests
    if not run_command("python test_app.py", "Running tests"):
        print("⚠️ Tests failed, but continuing with setup...")
    
    print("🎉 Local setup completed!")
    print("Run 'python app.py' to start the application")
    return True

def deploy_heroku(app_name=None):
    """Deploy to Heroku."""
    print("🚀 Deploying to Heroku...")
    
    if not check_prerequisites():
        return False
    
    # Check if Heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("Please install Heroku CLI first: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Login to Heroku
    if not run_command("heroku auth:whoami", "Checking Heroku authentication"):
        print("Please login to Heroku first: heroku login")
        return False
    
    # Create or use existing app
    if app_name:
        run_command(f"heroku create {app_name}", f"Creating Heroku app: {app_name}")
    
    # Add buildpack
    run_command("heroku buildpacks:set heroku/python", "Setting Python buildpack")
    
    # Deploy
    if not run_command("git add .", "Adding files to git"):
        return False
    
    if not run_command("git commit -m 'Deploy to Heroku'", "Committing changes"):
        print("No changes to commit or already committed")
    
    if not run_command("git push heroku main", "Pushing to Heroku"):
        return False
    
    print("🎉 Heroku deployment completed!")
    return True

def build_docker():
    """Build Docker image."""
    print("🐳 Building Docker image...")
    
    if not check_prerequisites():
        return False
    
    # Build Docker image
    if not run_command("docker build -t phishing-detector .", "Building Docker image"):
        return False
    
    print("🎉 Docker image built successfully!")
    print("Run 'docker run -p 5000:5000 phishing-detector' to start the container")
    return True

def run_docker():
    """Run Docker container."""
    print("🐳 Running Docker container...")
    
    if not run_command("docker run -p 5000:5000 phishing-detector", "Running Docker container"):
        return False
    
    return True

def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description='Deploy Phishing Email Detector')
    parser.add_argument('action', choices=['local', 'heroku', 'docker', 'docker-run'], 
                       help='Deployment action')
    parser.add_argument('--app-name', help='Heroku app name')
    
    args = parser.parse_args()
    
    print("🛡️ Phishing Email Detector Deployment")
    print("=" * 50)
    
    success = False
    
    if args.action == 'local':
        success = setup_local()
    elif args.action == 'heroku':
        success = deploy_heroku(args.app_name)
    elif args.action == 'docker':
        success = build_docker()
    elif args.action == 'docker-run':
        success = run_docker()
    
    print("=" * 50)
    if success:
        print("🎉 Deployment completed successfully!")
    else:
        print("❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
