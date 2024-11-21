from flask import Blueprint, jsonify, request, session
from app.models import PromptLog, db, ScrapedData
from app.utils import login_required, generete_response, scrape_url
from datetime import datetime
import time

main_bp = Blueprint("main", __name__)


@main_bp.route("/new-prompt", methods=['POST'])
@login_required
def handle_new_prompt():
    if request.method == "POST":
        data = request.get_json()
        prompt_text = data.get("prompt", "")
        user_id = session['google_user']['id']
        # user_id = '103165922844727225498'

        if not prompt_text:
            return jsonify({"error": "Prompt text is required"}), 400

        try:
            # Simulated delay
            time.sleep(1)  # 2 seconds delay

            output_text, tokens_used = generete_response(prompt_text=prompt_text)

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
            # app.logger.error(f"Error processing request: {e}")
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
            prompt_log = PromptLog.query.filter_by(
                created_by_user_id=user_id, 
                prompt_text=prompt_text
                ).first()
            
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
            prompt_logs = PromptLog.query.filter_by(
                created_by_user_id=user_id,
                prompt_text=prompt_text
                ).all()
            
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
            prompt_logs = PromptLog.query.filter_by(
                created_by_user_id=user_id, 
                prompt_text=prompt_text
                ).first()
            
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



@main_bp.route('/handle_scrape', methods=['GET', 'POST', 'DELETE'])
@login_required
def handle_scrape_data():
    if request.method == "GET":
        user_id = session['google_user']['id']
        try:
            # Find the prompt logs matching the user_id and prompt
            scrape_result = ScrapedData.query.filter_by(created_by_user_id=user_id).all()
            
            if not scrape_result:
                return jsonify({"message": "No matching urls found"}), 404
            
            urls = [ scrape.url for scrape in scrape_result ]
            return jsonify({"urls" : urls}) , 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500   
    
    elif request.method == "POST":
         # Get the user ID from session
        user_id = session['google_user']['id']
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "url not provided"}), 400
        url = data['url']
        try:
            scrape_result = ScrapedData.query.filter_by(created_by_user_id=user_id, url=url).first() 
            
            if not scrape_result:
                return jsonify({"message": "No matching url found"}), 404
            
            # Return scraped data as JSON
            return jsonify({
                'title': scrape_result.title,
                'description': scrape_result.description,
                'about':scrape_result.about,
                'name': scrape_result.name,
                'email': scrape_result.email,
                'contact': scrape_result.contact
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "DELETE":
        # Get the user ID from session
        user_id = session['google_user']['id']
        # Parse the input data to get the prompt
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "url not provided"}), 400
        
        url = data['url']

        try:
            scrape_results = ScrapedData.query.filter_by(created_by_user_id=user_id, url=url).all() 
            if not scrape_results:
                return jsonify({"message": "No matching url found"}), 404

            for scrape_result in scrape_results:
                db.session.delete(scrape_result)
            db.session.commit()

            return jsonify({"message": f"Deleted {len(scrape_results)} url(s) successfully"}), 200

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            return jsonify({"error": str(e)}), 500

    


@main_bp.route('/scrape', methods=['POST'])
@login_required
def scrape():
    if request.method == 'POST':
        data = request.json
        url = data.get('url')        
        user_id = session['google_user']['id']
        scrape_result = scrape_url(url)  # scrape_url() is the scraping logic function
        if 'error' in scrape_result:
            return jsonify({'error': scrape_result['error']}), 500

        # Save to database
        scraped_data = ScrapedData(
            created_by_user_id=user_id,
            url=url,
            title=scrape_result['title'],
            description=scrape_result['description'],
            name=scrape_result['name'],
            about=scrape_result['about'],
            source=scrape_result['source'],
            industry=scrape_result['industry'],
            page_content_type=scrape_result['page_content_type'],
            contact=scrape_result['contact'],
            email=scrape_result['email']
        )
        db.session.add(scraped_data)
        db.session.commit()

        # Return scraped data as JSON
        return jsonify({
            'title': scrape_result.get('title', 'N/A'),
            'description': scrape_result.get('description', 'N/A'),
            'about':scrape_result.get('about', 'N/A'),
            'name': scrape_result.get('name', 'N/A'),
            'email': scrape_result.get('email', 'N/A'),
            'contact': scrape_result.get('contact', 'N/A')
        }), 200


