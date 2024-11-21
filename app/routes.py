from flask import Blueprint, jsonify, request, session, render_template
from app.models import PromptLog, db
from app.utils import login_required, generete_response
from datetime import datetime
import time

import threading
lock = threading.Lock()

def synchronized(func):
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """
    Render login page if user is not logged in, otherwise show dashboard.
    """
    if "google_user" in session:
        return render_template("dashboard.html", user=session["google_user"])
    return render_template("login.html")

@main_bp.route("/new-prompt", methods=['POST'])
@login_required
def handle_new_prompt():
    if request.method == "POST":
        data = request.get_json()
        prompt_text = data.get("prompt", "")
        user_id = session['google_user']['id']
        output_text, tokens_used = generete_response(prompt_text=prompt_text)
        
        if not prompt_text:
            return jsonify({"error": "Prompt text is required"}), 400
        try:
            # Simulated response

            # Save to database
            prompt_log = PromptLog(
                prompt_text=prompt_text,
                generated_output=output_text,
                tokens_used=tokens_used,
                created_by_user_id=user_id,
                created_at=datetime.utcnow(),
            )
            db.session.add(prompt_log)
            db.session.commit()

            return jsonify({
                "prompt": prompt_text,
                "response": output_text,
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

@main_bp.route("/prompt", methods=["DELETE","POST","GET","PUT"])
@login_required
def handle_prompt():
    if request.method == "GET":
        user_id = session['google_user']['id']
        try:
            # Find the prompt logs matching the user_id and prompt
            prompt_log = PromptLog.query.filter_by(created_by_user_id=user_id).all()
            
            if not prompt_log:
                return jsonify({"message": "No matching prompts found"}), 404
            
            prompts = [ prompt.prompt_text for prompt in prompt_log ]
            return jsonify({'prompts': prompts}) , 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "POST":
         # Get the user ID from session
        user_id = session['google_user']['id']
        # Parse the input data to get the prompt
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt not provided"}), 400
        
        prompt_text = data['prompt']

        try:
            # Find the prompt logs matching the user_id and prompt
            prompt_log = PromptLog.query.filter_by(created_by_user_id=user_id, prompt_text=prompt_text).first()
            
            if not prompt_log:
                return jsonify({"message": "No matching prompts found"}), 404
            
            return jsonify({
                'prompt': prompt_log.prompt_text,
                "response": prompt_log.generated_output}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "DELETE":
        # Get the user ID from session
        user_id = session['google_user']['id']
        # Parse the input data to get the prompt
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt not provided"}), 400
        
        prompt_text = data['prompt']

        try:
            # Find the prompt logs matching the user_id and prompt
            prompt_logs = PromptLog.query.filter_by(created_by_user_id=user_id, prompt_text=prompt_text).all()
            
            if not prompt_logs:
                return jsonify({"message": "No matching prompts found"}), 404

            # Delete the matching rows
            for prompt_log in prompt_logs:
                db.session.delete(prompt_log)

            db.session.commit()

            return jsonify({"message": f"Deleted {len(prompt_logs)} prompt(s) successfully"}), 200

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return jsonify({"error": str(e)}), 500

    elif request.method == "PUT":
        # Get the user ID from session
        user_id = session['google_user']['id']
        # Parse the input data to get the prompt
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt not provided"}), 400
        
        prompt_text = data['prompt']

        try:
            # Find the prompt logs matching the user_id and prompt
            prompt_logs = PromptLog.query.filter_by(created_by_user_id=user_id, prompt_text=prompt_text).first()
            
            if not prompt_logs:
                return jsonify({"message": "No matching prompts found"}), 404

            output_text, tokens_used = generete_response(prompt_text=prompt_text)

            prompt_logs.prompt_text=prompt_text,
            prompt_logs.generated_output=output_text,
            prompt_logs.tokens_used=tokens_used,
            prompt_logs.created_at=datetime.utcnow(),
            
            db.session.commit()
            return jsonify({
                "prompt": prompt_text,
                "response": output_text,
            }), 200
        
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return jsonify({"error": str(e)}), 500


@main_bp.route("/home")
@login_required
def home():
    """
    Render the chatbot UI.
    """
    return render_template("home.html")


