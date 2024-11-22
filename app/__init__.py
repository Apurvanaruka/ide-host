from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

load_dotenv()


# Existing imports
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # OAuth setup
    google_bp = make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        redirect_url="/google",
        scope=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Initialize extensions
    Session(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(google_bp, url_prefix="/auth")
    
    # Register blueprints
    from app.auth import auth_bp
    from app.routes import main_bp
    from app.view import view_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(view_bp)

    return app
