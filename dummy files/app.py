# File: app.py (Updated)

from flask import Flask,redirect,url_for,  request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
from flask_session import Session
import os
from datetime import datetime
# from langchain.chat_models import ChatOpenAI  # Ensure this is the correct module
# from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

app.secret_key = "your_secret_key"  # Replace with a strong secret key
app.config["SESSION_TYPE"] = "filesystem"

# Flask-Session setup
Session(app)

# Allow HTTP in development for OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:admin@localhost/user_db' # os.getenv('DATABASE_URL')  # e.g., 'postgresql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth Configuration
google_bp = make_google_blueprint(
    client_id="975512642838-61a9v7bmogtccbdu2b0jqkq8bbq3c0bd.apps.googleusercontent.com",
    client_secret="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",
    redirect_url="/google",
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
)
app.register_blueprint(google_bp, url_prefix="/google_login")

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# # OpenAI API Configuration
# openai_api_key = os.getenv('OPENAI_API_KEY')
# llm = ChatOpenAI(openai_api_key=openai_api_key)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    social_login_provider = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    prompt_logs = db.relationship('PromptLog', backref='user', lazy=True)


class PromptLog(db.Model):
    __tablename__ = 'prompt_logs'

    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    generated_output = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, nullable=True)  # Tokens might not always be available
    created_by_user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Database initialization route (for testing)
@app.route('/init-db')
def init_db():
    """
    Create all tables in the database. Use this route to initialize the database.
    """
    db.create_all()
    return "Database and tables created successfully!"


@app.route('/')
def index():
  if session:
    return render_template('index.html', user=session['google_user'])
  else:
    return render_template('login.html')

@app.route('/home')
def home():
    if session:
        return render_template('home.html')
    else:
        return render_template('login.html')


# Endpoint for prompt-based interaction
@app.route('/prompt', methods=['POST'])
def handle_prompt():
    """
    Handle a user prompt and generate a response using LangChain.
    Save the prompt and response in the PromptLog table.
    """
    # # Parse request data
    data = request.get_json()
    prompt_text = data.get('prompt', '')
    user_id = 1  # Assume user ID is provided in the request

    if not prompt_text or not user_id:
        return jsonify({"error": "Prompt and user_id are required."}), 400
    
    try:
        # Generate a response using LangChain
        # messages = [HumanMessage(content=prompt_text)]
        # response = llm(messages)
        output_text =  'this is dummy response' # response.content  # Extract generated text
        tokens_used = 5  # LangChain might not provide token usage directly

        # Save prompt and response to database
        prompt_log = PromptLog(
            prompt_text=prompt_text,
            generated_output=output_text,
            tokens_used=tokens_used,
            created_by_user_id=user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(prompt_log)
        db.session.commit()

        return jsonify({
            "prompt": prompt_text,
            "response": output_text,
            "tokens_used": tokens_used or "N/A"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')



@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        user_info = resp.json()
        print(user_info)
        session["google_user"] = user_info  # Store user info in session

        # Extract data
        user_id = user_info.get("id")
        name = user_info.get("name")
        email = user_info.get("email")
        picture = user_info.get("picture")

        # Check if user exists in the database
        user = User.query.filter_by(email=email).first()

        if user:
            # Update existing user info if needed
            user.name = name
            user.profile_picture = picture
            user.social_login_provider = "google"
        else:
            # Create a new user
            user = User(
                name=name,
                email=email,
                social_login_provider="google",
                profile_picture=picture,
            )

        db.session.add(user)
        # Commit changes
        db.session.commit()
        return render_template('index.html', user=session['google_user'])

    return render_template('login.html')
    
 


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
