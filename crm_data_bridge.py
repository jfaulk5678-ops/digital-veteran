import logging
import os
import secrets
from functools import wraps

from flask import Flask, jsonify, redirect, request, session
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

# Environment variables
CLIENT_SECRETS_FILE = os.environ.get("CLIENT_SECRETS_FILE", "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://yourdomain.com/oauth2callback")

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "credentials" not in session:
            return redirect("/authorize")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return "Google API Integration"


@app.route("/authorize")
def authorize():
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        session["state"] = state
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        return jsonify(error="Authorization failed"), 500


@app.route("/oauth2callback")
def oauth2callback():
    try:
        state = session["state"]
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        session["credentials"] = credentials_to_dict(credentials)
        return redirect("/protected")
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return jsonify(error="Authentication failed"), 401


@app.route("/protected")
@login_required
def protected():
    try:
        credentials = Credentials(**session["credentials"])
        service = build("gmail", "v1", credentials=credentials)
        results = service.users().messages().list(userId="me").execute()
        return jsonify(messages=results.get("messages", []))
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return jsonify(error="Service unavailable"), 503


@app.route("/revoke")
def revoke():
    try:
        credentials = Credentials(**session["credentials"])
        credentials.revoke(Request())
        session.clear()
        return jsonify(message="Credentials revoked")
    except Exception as e:
        logger.error(f"Revocation error: {str(e)}")
        return jsonify(error="Revocation failed"), 500


@app.route("/clear")
def clear_credentials():
    session.clear()
    return jsonify(message="Session cleared")


if __name__ == "__main__":
    app.run(ssl_context="adhoc", host="0.0.0.0", port=5000)
