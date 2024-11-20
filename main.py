
# File: app.py

from flask import Flask, redirect, url_for, render_template, session
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_session import Session
import os  # For setting environment variable

# Flask app configuration
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
app.config["SESSION_TYPE"] = "filesystem"

# Flask-Session setup
Session(app)

# Allow HTTP in development for OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Google OAuth Configuration
google_bp = make_google_blueprint(
    client_id="975512642838-61a9v7bmogtccbdu2b0jqkq8bbq3c0bd.apps.googleusercontent.com",
    client_secret="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",
    redirect_url="/google/authorized",
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
)
# Google OAuth Configuration
# google_bp = make_google_blueprint(
#     client_id="your_google_client_id",
#     client_secret="your_google_client_secret",
#     redirect_url="/google/authorized",
#     scope=["profile", "email"],
# )
app.register_blueprint(google_bp, url_prefix="/google_login")

# Facebook OAuth Configuration
facebook_bp = make_facebook_blueprint(
    client_id="your_facebook_app_id",
    client_secret="your_facebook_app_secret",
    redirect_url="/facebook/authorized",
)
app.register_blueprint(facebook_bp, url_prefix="/facebook_login")

# Routes
@app.route("/")
def home():
    return render_template("home.html")  # Create a home.html with login links

@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        user_info = resp.json()
        print(user_info)
        session["google_user"] = user_info  # Store user info in session
        return f"Logged in as: {user_info['email']}<br><a href='/logout'>Logout</a>"
    return "Google login failed!"

@app.route("/facebook")
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("/me?fields=id,name,email")
    if resp.ok:
        user_info = resp.json()
        session["facebook_user"] = user_info  # Store user info in session
        return f"Logged in as: {user_info['email']}<br><a href='/logout'>Logout</a>"
    return "Facebook login failed!"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
