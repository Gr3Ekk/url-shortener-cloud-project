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

def test_valid_url_shortening(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_custom_alias_shortening(client):
    alias = 'custom123'
    response = client.post('/api/shorten', json={
        'url': 'https://custom.com',
        'custom_alias': alias
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['short_code'] == alias

def test_duplicate_custom_alias(client):
    alias = 'dupealias'
    client.post('/api/shorten', json={
        'url': 'https://first.com',
        'custom_alias': alias
    })

    # Try to reuse the alias
    response = client.post('/api/shorten', json={
        'url': 'https://second.com',
        'custom_alias': alias
    })
    assert response.status_code == 409 or response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_invalid_url_format(client):
    response = client.post('/api/shorten', json={'url': 'not-a-valid-url'})
    assert response.status_code == 400 or response.status_code == 422
    data = response.get_json()
    assert 'error' in data

def test_missing_url_parameter(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_malformed_json_request(client):
    response = client.post('/api/shorten', data="This is not JSON", content_type='application/json')
    assert response.status_code == 400

def test_database_connection_error(monkeypatch, client):
    from config.mock_database import MockURLMapping

    def raise_error(*args, **kwargs):
        raise Exception("Mock DB failure")

    monkeypatch.setattr(MockURLMapping, "create_mapping", raise_error)

    response = client.post('/api/shorten', json={'url': 'https://fail.com'})
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
