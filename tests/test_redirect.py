import pytest
import os
from app import create_app
from config.mock_database import MockURLMapping


@pytest.fixture
def client(monkeypatch):
    os.environ['USE_MOCK_DATABASE'] = 'true'
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_short_url(client):
    def _create(url):
        response = client.post('/api/shorten', json={'url': url})
        assert response.status_code == 200
        data = response.get_json()
        return data['short_code'], data['short_url']
    return _create

def test_valid_redirect(client, create_short_url):
    original_url = "https://example.com"
    short_code, _ = create_short_url(original_url)

    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'] == original_url

def test_invalid_short_code_404(client):
    response = client.get('/nonexistent123', follow_redirects=False)
    assert response.status_code == 404

def test_click_counter_increment(client, create_short_url):
    short_code, _ = create_short_url("https://example.com")

    # First click
    response = client.get(f'/{short_code}')
    assert response.status_code == 302

    # Access mock database directly
    from config.mock_database import MockURLMapping
    mapping = MockURLMapping.get_mapping(short_code)
    assert mapping['click_count'] == 1

    # Another click
    client.get(f'/{short_code}')
    mapping = MockURLMapping.get_mapping(short_code)
    assert mapping['click_count'] == 2

def test_malformed_short_code(client):
    response = client.get('/!@#$', follow_redirects=False)
    assert response.status_code in (400, 404)  # Depends how you handle this in your code

def test_end_to_end_flow(client, create_short_url):
    url = "https://endtoend.com"
    short_code, short_url = create_short_url(url)

    redirect_response = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.headers['Location'] == url
