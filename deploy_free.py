# deploy_free.py
import os
import webbrowser

def show_deployment_options():
    """Show all free deployment options"""
    print("?? FREE DEPLOYMENT OPTIONS")
    print("="*50)
    
    options = {
        "1": {"name": "Railway.app", "desc": "Easiest Python hosting", "cmd": "python deploy_railway.py"},
        "2": {"name": "Render.com", "desc": "Great free tier", "cmd": "python deploy_render.py"},
        "3": {"name": "PythonAnywhere", "desc": "Traditional Python hosting", "cmd": "python deploy_pythonanywhere.py"},
        "4": {"name": "GitHub Pages", "desc": "Static demo version", "cmd": "python create_static_demo.py"},
        "5": {"name": "Vercel", "desc": "Fast frontend hosting", "cmd": "python deploy_vercel.py"}
    }
    
    for key, option in options.items():
        print(f"{key}. {option['name']} - {option['desc']}")
    
    choice = input("\n?? Choose deployment option (1-5): ").strip()
    
    if choice in options:
        os.system(options[choice]['cmd'])
    else:
        print("? Invalid choice")

def quick_deploy():
    """Quick deploy to the easiest option"""
    print("? Quick deploying to Railway.app (recommended)...")
    
    # Create minimal configuration
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            f.write('Flask==2.3.3\nrequests==2.31.0\n')
    
    # Simple deployment instructions
    print("""
?? QUICK DEPLOYMENT:

1. Push your code to GitHub
2. Go to: https://railway.app
3. Click 'New Project'
4. Select 'Deploy from GitHub'
5. Choose your repository
6. Railway auto-deploys!

?? Your app will be live at: https://your-app-name.railway.app

?? For immediate testing, run locally:
   python dashboard.py
   # Then visit: http://localhost:5000
""")
    
    webbrowser.open('https://railway.app')

if __name__ == "__main__":
    print("?? Digital Veteran Free Deployment")
    
    if input("Quick deploy? (y/n): ").lower().startswith('y'):
        quick_deploy()
    else:
        show_deployment_options()
