import google.generativeai as genai
from flask import session, jsonify, render_template, session
from functools import wraps
from time import time
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


async def generete_response(prompt_text):
    await time.sleep(200)
    return "this is updated response", 300 # early return

    # model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content(prompt_text)
    # print(response.text)
    # return response.text, response.usage_metadata.total_token_count

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
            session.clear()
            return render_template("login.html")


        # Check for google_user key in session
        google_user = session.get("google_user")
        if not google_user:
            return jsonify({"error": "Authentication required"}), 403

        # If all checks pass, proceed to the wrapped function
        return f(*args, **kwargs)

    return decorated_function
