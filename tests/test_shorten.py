# TODO: DERRICK - Test Cases for URL Shortening API
"""
TASKS FOR DERRICK:
1. Write test cases for the shortening API endpoint
2. Test valid URL shortening
3. Test invalid URL handling
4. Test custom alias functionality
5. Test duplicate alias handling
6. Test rate limiting (if implemented)
7. Integration testing with database

REQUIRED TEST SCENARIOS:
- Valid URL shortening with auto-generated code
- Valid URL with custom alias
- Invalid URL format handling
- Duplicate custom alias error
- Missing URL in request
- Malformed JSON request
- Database connection errors

DEPENDENCIES:
- Requires Luis's implementation of routes/shorten.py
- Requires Luis's database setup in models/url_mapping.py
- Requires proper test database configuration

EXAMPLE STRUCTURE:
import pytest
import json
from app import app  # Main Flask app
from config.database import init_db

class TestShortenAPI:
    @pytest.fixture
    def client(self):
        # Set up test client
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_valid_url_shortening(self, client):
        # Test successful URL shortening
        pass
    
    def test_custom_alias_shortening(self, client):
        # Test URL shortening with custom alias
        pass
    
    def test_invalid_url_format(self, client):
        # Test error handling for invalid URLs
        pass
    
    def test_duplicate_custom_alias(self, client):
        # Test duplicate alias handling
        pass
    
    def test_missing_url_parameter(self, client):
        # Test missing required parameters
        pass
"""

# DERRICK: Replace this comment block with actual test code
