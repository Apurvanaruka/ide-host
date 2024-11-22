import google.generativeai as genai
from flask import session, jsonify, render_template, session
from functools import wraps
from time import time
import os
from dotenv import load_dotenv, find_dotenv
import requests
from bs4 import BeautifulSoup
import re

load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def generete_response(prompt_text):
    return "this is updated response", 300 # early return
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt_text)
    print(response.text)
    return response.text, response.usage_metadata.total_token_count

# Web scraper function
def scrape_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        title = soup.title.string if soup.title else None
        description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        description = description['content'] if description else None

        # Custom logic to extract other fields
        name = soup.find('h1').text if soup.find('h1') else None
        contact = re.search(r'\b\d{10}\b', soup.text)
        contact = contact.group(0) if contact else None
        email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.text)
        email = email.group(0) if email else None
        # return {
        #     'title': 'title',
        #     'description': 'description',
        #     'name': 'name',
        #     'about': """ Objective Design and implement a Flask application that integrates Flask-SQLAlchemy (with
        #             PostgreSQL) to build a small web application. The project should also include features for
        #             prompting using LangChain, web scraping, and social login authentication.
        #             Assignment Requirements:
        #             1. Database Setup (PostgreSQL):
        #             o Create a database using PostgreSQL.
        #             o Define the following models using Flask-SQLAlchemy:
        #             ▪ User: For managing users (name, email, social_login_provider,
        #             profile_picture, created_at).
        #             ▪ ScrapedData: For storing data scraped from a website (URL, content,
        #             metadata, created_by_user_id as a foreign key to User, and created_at).
        #             ▪ PromptLog: For storing prompts and their generated outputs
        #             (prompt_text, generated_output, created_by_user_id as a foreign key to
        #             User, and created_at).""",
        #     'source': None,
        #     'industry': None,
        #     'page_content_type': 'HTML',
        #     'contact': 'contact',
        #     'email': 'apurvanaruka@gmail.com'
        # }

        return {
            'title': title,
            'description': description,
            'name': name,
            'about': None,
            'source': None,
            'industry': None,
            'page_content_type': 'HTML',
            'contact': contact,
            'email': email
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


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

