from flask import Blueprint, redirect, url_for, session, render_template
from flask_dance.contrib.google import google
from app.models import User
from app import db

# Load environment variables
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        user_info = resp.json()
        session["google_user"] = user_info
        # Extract user details
        id=user_info.get('id')
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")

        # Check or create user in database
        user = User.query.filter_by(email=email).first()
    
        if user:
            user.id=id
            user.name = name
            user.profile_picture = picture
            user.social_login_provider = "google"
        else:
            user = User(
                id = id,
                name=name,
                email=email,
                social_login_provider="google",
                profile_picture=picture,
            )
        db.session.add(user)
        db.session.commit()

        return render_template("index.html", user=session["google_user"])

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("view.index"))
