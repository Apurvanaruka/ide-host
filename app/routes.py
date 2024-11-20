from flask import Blueprint, jsonify, request, session, render_template
from app.models import PromptLog, db
from app.utils import login_required
from datetime import datetime

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """
    Render login page if user is not logged in, otherwise show dashboard.
    """
    if "google_user" in session:
        return render_template("dashboard.html", user=session["google_user"])
    return render_template("login.html")


@main_bp.route("/prompt", methods=["POST"])
@login_required
def handle_prompt():
    data = request.get_json()
    prompt_text = data.get("prompt", "")
    user_id = session['google_user']['id']

    if not prompt_text:
        return jsonify({"error": "Prompt text is required"}), 400

    try:
        # Simulated response
        output_text = "This is a dummy response"
        tokens_used = 5

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
            "tokens_used": tokens_used
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/home")
@login_required
def home():
    """
    Render the chatbot UI.
    """
    return render_template("home.html")


