from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(50), primary_key=True) 
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    social_login_provider = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    prompt_logs = db.relationship("PromptLog", backref="user", lazy=True)


class PromptLog(db.Model):
    __tablename__ = "prompt_logs"

    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    generated_output = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, nullable=True)
    created_by_user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class ScrapedData(db.Model):
    __tablename__ = 'scraped_data'
    id = db.Column(db.Integer, primary_key=True)
    created_by_user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    name = db.Column(db.String(250))
    about = db.Column(db.Text)
    source = db.Column(db.String(250))
    industry = db.Column(db.String(100))
    page_content_type = db.Column(db.String(100))
    contact = db.Column(db.String(250))
    email = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)