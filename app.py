# File: app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # e.g., 'postgresql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    social_login_provider = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    scraped_data = db.relationship('ScrapedData', backref='user', lazy=True)
    prompt_logs = db.relationship('PromptLog', backref='user', lazy=True)


class ScrapedData(db.Model):
    __tablename__ = 'scraped_data'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=True)
    metadata = db.Column(db.Text, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PromptLog(db.Model):
    __tablename__ = 'prompt_logs'

    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    generated_output = db.Column(db.Text, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Database initialization route (for testing)
@app.route('/init-db')
def init_db():
    """
    Create all tables in the database. Use this route to initialize the database.
    """
    db.create_all()
    return "Database and tables created successfully!"


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
