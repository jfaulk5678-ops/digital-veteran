# deploy_production.py
import os
import subprocess


def deploy_production():
    """Deploy Digital Veteran to production"""
    print("?? Deploying Digital Veteran to Production...")

    # Check if we have the necessary files
    required_files = ["Dockerfile", "docker-compose.yml", "requirements.txt"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"? Missing required file: {file}")
            return False

    # Check if .env exists, if not create from template
    if not os.path.exists(".env"):
        if os.path.exists(".env.template"):
            print("??  .env file not found. Creating from template...")
            os.system("cp .env.template .env")
            print("? Created .env file. Please update with your API keys.")
        else:
            print("? Missing .env.template file")
            return False

    # Build and deploy with Docker
    try:
        print("?? Building Docker image...")
        subprocess.run(["docker", "compose", "build"], check=True)

        print("?? Starting services...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)

        print("? Deployment successful!")
        print("?? Dashboard available at: http://localhost:5000")
        print("?? Check logs with: docker compose logs -f")

    except subprocess.CalledProcessError as e:
        print(f"? Deployment failed: {e}")
        return False

    return True


if __name__ == "__main__":
    deploy_production()
