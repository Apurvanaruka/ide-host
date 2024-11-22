from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_dance.contrib.google import make_google_blueprint
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from flask_migrate import Migrate

load_dotenv()

# Existing imports
db = SQLAlchemy()
migrate = Migrate()

def create_database_if_not_exists(database_url):
    """Check and create the database if it doesn't exist."""
    server_url = database_url.rsplit("/", 1)[0]  # Connect to the server, excluding the database name
    db_name = database_url.rsplit("/", 1)[-1]
    engine = create_engine(server_url, isolation_level="AUTOCOMMIT")  # Set autocommit mode
    with engine.connect() as conn:
        try:
            # Check if the database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
            if not result.fetchone():
                # Create the database if it doesn't exist
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
        except ProgrammingError as e:
            print(f"Error checking or creating the database: {e}")

def create_app():
    app = Flask(__name__)

    # App configuration
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Check and create database if not exists
    create_database_if_not_exists(app.config["SQLALCHEMY_DATABASE_URI"])

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
