# deploy_railway.py
import os
import subprocess
import webbrowser

def deploy_railway():
    """Deploy to Railway.app for free"""
    print("?? Deploying to Railway.app...")
    
    # Check if Railway CLI is installed
    try:
        subprocess.run(['railway', '--version'], capture_output=True, check=True)
    except:
        print("? Railway CLI not installed.")
        print("?? Install with: npm install -g @railway/cli")
        print("?? Or deploy via GitHub: https://railway.app")
        return False
    
    # Login to Railway
    print("?? Logging into Railway...")
    subprocess.run(['railway', 'login'], check=True)
    
    # Initialize Railway project
    print("?? Initializing project...")
    subprocess.run(['railway', 'init'], check=True)
    
    # Deploy
    print("?? Deploying...")
    result = subprocess.run(['railway', 'deploy'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("? Deployment successful!")
        
        # Get the deployed URL
        url_result = subprocess.run(['railway', 'status'], capture_output=True, text=True)
        print(url_result.stdout)
        
        # Open in browser
        webbrowser.open('https://railway.app')
    else:
        print("? Deployment failed")
        print(result.stderr)

if __name__ == "__main__":
    deploy_railway()
