# app.py - Main application file
import os

from waitress import serve

from dashboard import app


def run_production():
    """Run with Waitress production server"""
    port = int(os.environ.get("PORT", 5000))
    print(f"?? Starting Waitress production server on port {port}")
    serve(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    run_production()
