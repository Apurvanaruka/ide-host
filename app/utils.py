from flask import session, jsonify
from functools import wraps
from time import time

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the Google OAuth token exists in the session
        google_oauth_token = session.get("google_oauth_token")
        if not google_oauth_token:
            return jsonify({"error": "Authentication required"}), 403

        # Validate token expiration
        expires_at = google_oauth_token.get("expires_at")
        if not expires_at or expires_at < time():
            return jsonify({"error": "Token has expired. Please log in again."}), 401

        # Check for google_user key in session
        google_user = session.get("google_user")
        if not google_user:
            return jsonify({"error": "Authentication required"}), 403

        # If all checks pass, proceed to the wrapped function
        return f(*args, **kwargs)

    return decorated_function
