print("?? YOUR APP IS LOCAL - LET'S DEPLOY IT ONLINE!")
print("=" * 50)
print("Current: http://10.135.59.12:5000 (Local only)")
print("Goal: https://your-app.railway.app (Public online)")

print("\n?? DEPLOYMENT STEPS:")
print("1. Go to: https://railway.app/new")
print("2. Select 'Deploy from GitHub repo'")
print("3. Choose 'jfaulk5678-ops/digital-veteran'")
print("4. Wait for build to complete (2-3 minutes)")
print("5. Get your PUBLIC URL from Railway dashboard")

print("\n?? What you'll see after deployment:")
print("   ? Build logs showing successful installation")
print("   ? Public URL like: https://digital-veteran.up.railway.app")
print("   ? Accessible from anywhere in the world")

print("\n?? While Railway builds, let's verify your app:")
import requests

try:
    response = requests.get("http://localhost:5000/api/stats", timeout=2)
    print("? Local app is running correctly")
except:
    print("??  Local app not running - start with: python dashboard.py")

import webbrowser

webbrowser.open("https://railway.app/new")
