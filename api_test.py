# tests/test_api.py

import pytest
from app import create_app, db
from app.models import PromptLog, ScrapedData

@pytest.fixture
def client():
    app = create_app()  # Use a config for testing
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Set up the test database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Tear down the test database

@pytest.fixture
def mock_login_session(monkeypatch):
    # Mock session for logged-in user
    monkeypatch.setattr('flask.session', {'google_user': {'id': 'test_user_id'}})

def test_handle_new_prompt(client, mock_login_session):
    # Test POST /new-prompt with valid input
    response = client.post('/new-prompt', json={'prompt': 'Test prompt'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['prompt'] == 'Test prompt'

    # Test POST /new-prompt with missing input
    response = client.post('/new-prompt', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Prompt text is required'

def test_handle_prompt_get(client, mock_login_session):
    # Seed test data
    prompt_log = PromptLog(
        prompt_text="Example prompt",
        generated_output="Generated response",
        tokens_used=10,
        created_by_user_id="test_user_id"
    )
    db.session.add(prompt_log)
    db.session.commit()

    # Test GET /prompt
    response = client.get('/prompt')
    assert response.status_code == 200
    data = response.get_json()
    assert 'prompts' in data
    assert "Example prompt" in data['prompts']

def test_handle_prompt_post(client, mock_login_session):
    # Seed test data
    prompt_log = PromptLog(
        prompt_text="Example prompt",
        generated_output="Generated response",
        tokens_used=10,
        created_by_user_id="test_user_id"
    )
    db.session.add(prompt_log)
    db.session.commit()

    # Test POST /prompt with matching data
    response = client.post('/prompt', json={'prompt': 'Example prompt'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['prompt'] == 'Example prompt'
    assert data['response'] == 'Generated response'

    # Test POST /prompt with no matching data
    response = client.post('/prompt', json={'prompt': 'Non-existent prompt'})
    assert response.status_code == 404
    assert response.get_json()['message'] == 'No matching prompts found'

def test_handle_prompt_delete(client, mock_login_session):
    # Seed test data
    prompt_log = PromptLog(
        prompt_text="Example prompt",
        generated_output="Generated response",
        tokens_used=10,
        created_by_user_id="test_user_id"
    )
    db.session.add(prompt_log)
    db.session.commit()

    # Test DELETE /prompt with valid data
    response = client.delete('/prompt', json={'prompt': 'Example prompt'})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Deleted 1 prompt(s) successfully'

    # Test DELETE /prompt with no matching data
    response = client.delete('/prompt', json={'prompt': 'Non-existent prompt'})
    assert response.status_code == 404
    assert response.get_json()['message'] == 'No matching prompts found'

def test_scrape(client, mock_login_session):
    # Mock scrape_url function
    def mock_scrape_url(url):
        return {
            'title': 'Mock Title',
            'description': 'Mock Description',
            'name': 'Mock Name',
            'about': 'Mock About',
            'source': 'Mock Source',
            'industry': 'Mock Industry',
            'page_content_type': 'Mock Content',
            'contact': 'Mock Contact',
            'email': 'mock@example.com'
        }

    from app.utils import scrape_url
    client.application.app_context().push()
    scrape_url = mock_scrape_url

    # Test POST /scrape with valid data
    response = client.post('/scrape', json={'url': 'http://google.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Mock Title'
    assert data['email'] == 'mock@example.com'

    # Test POST /scrape with missing URL
    response = client.post('/scrape', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'url not provided'
