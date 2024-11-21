from flask import Blueprint, session, render_template
from app.utils import login_required

view_bp = Blueprint("view", __name__)



@view_bp.route("/")
def index():
    """
    Render login page if user is not logged in, otherwise show index.
    """
    if "google_user" in session:
        return render_template("index.html", user=session["google_user"])
    return render_template("login.html")


@view_bp.route("/scraperpage")
@login_required
def scraper():
    """
    Render the chatbot UI.
    """
    return render_template("scraper.html",user=session["google_user"])

@view_bp.route("/promptpage")
@login_required
def promptpage():
    """
    Render the chatbot UI.
    """
    return render_template("prompt.html",user=session["google_user"])

